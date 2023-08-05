.. module:: streamsets

Usage instructions
==================

The examples below assume you've installed the ``streamsets`` library,
:ref:`activated the library <activation>`, and are inside a Python 3.4+ interpreter.


Use of the SDK begins by importing the library. For convenience,
we tend to directly import the classes we need:

.. code-block:: python

    >>> from streamsets.sdk import DataCollector

Next, create an instance of :py:class:`streamsets.sdk.DataCollector`, passing in
the URL of your StreamSets Data Collector instance:

.. code-block:: python

    >>> data_collector = DataCollector('http://localhost:18630')

Credentials
-----------

If no user credentials are passed to :py:class:`streamsets.sdk.DataCollector` when it's being instantiated,
:py:attr:`streamsets.sdk.sdc.DEFAULT_SDC_USERNAME` and :py:attr:`streamsets.sdk.sdc.DEFAULT_SDC_PASSWORD` will be
used for the ``username`` and ``password`` arguments, respectively. If your Data Collector instance is
registered with StreamSets Control Hub, your Control Hub credentials need to be used to instantiate an instance
of :py:class:`streamsets.sdk.ControlHub` before it's passed as an argument to :py:class:`streamsets.sdk.DataCollector`
instead:

.. code-block:: python

    >>> from streamsets.sdk import ControlHub
    >>> control_hub = ControlHub('https://cloud.streamsets.com',
                                 username=<your username>,
                                 password=<your password>)
    >>> data_collector = DataCollector('http://localhost:18630', control_hub=control_hub)


Getting ID
----------
Next, you can get the ID for the StreamSets Data Collector instance.

.. code-block:: python

    >>> data_collector.id
    a67344ff-72e9-11ea-af9c-ff111e534c98

Creating a pipeline
-------------------

Next, you can now get an instance of :py:class:`streamsets.sdk.sdc_models.PipelineBuilder`:

.. code-block:: python

    >>> builder = data_collector.get_pipeline_builder()

We get :py:class:`streamsets.sdk.sdc_models.Stage` instances from this builder by calling
:py:meth:`streamsets.sdk.sdc_models.PipelineBuilder.add_stage`.

See the API reference for this method for details on the arguments it takes.

As shown in the :ref:`first example <first-example>`, the simplest type of pipeline
directs one origin into one destination. For this example, we do this with ``Dev Raw Data Source``
origin and ``Trash`` destination, respectively:

.. code-block:: python

    >>> dev_raw_data_source = builder.add_stage('Dev Raw Data Source')
    >>> trash = builder.add_stage('Trash')

With :py:class:`streamsets.sdk.sdc_models.Stage` instances in hand, we can connect them by using the ``>>`` operator,
and then building a :py:class:`streamsets.sdk.sdc_models.Pipeline` instance with the
:py:meth:`streamsets.sdk.sdc_models.PipelineBuilder.build` method:

.. code-block:: python

    >>> dev_raw_data_source >> trash
    >>> pipeline = builder.build('My first pipeline')

Finally, to add this pipeline to your Data Collector instance, pass it to the
:py:meth:`streamsets.sdk.DataCollector.add_pipeline` method:

.. code-block:: python

    >>> data_collector.add_pipeline(pipeline)


Configuring stages
------------------

In practice, it's rare to have stages in your pipeline that haven't had some configurations
changed from their default values. When using the SDK, the names to use when referring
to these configuration properties can generally be inferred from the StreamSets Data Collector UI (e.g.
``Data Format`` becomes ``data_format``), but they can also be directly inspected in a Python
interpreter using the :py:func:`dir` built-in function on an instance of the
:py:class:`streamsets.sdk.sdc_models.Stage` class:

.. code-block:: python

    >>> dir(dev_raw_data_source)

or by using Python's built-in :py:func:`help` function:

.. code-block:: python

    >>> help(dev_raw_data_source)

.. image:: _static/dev_raw_data_source_help.png

With the attribute name in hand, you can read the value of the configuration:

.. code-block:: python

    >>> dev_raw_data_source.max_line_length
    1024

As for setting the value of the configuration, this can be done in one of two ways
depending on your use case:


Single configurations
~~~~~~~~~~~~~~~~~~~~~

If you only have one or two configurations to update, you can set them using attributes of the
:py:class:`streamsets.sdk.sdc_models.Stage` instance. Continuing in the vein of our example:

.. code-block:: python

    >>> dev_raw_data_source.data_format = 'TEXT'
    >>> dev_raw_data_source.raw_data = 'hi\nhello\nhow are you?'

Multiple configurations
~~~~~~~~~~~~~~~~~~~~~~~

For readability, it's sometimes better to set all attributes simultaneously with
one call to the :py:meth:`streamsets.sdk.sdc_models.Stage.set_attributes` method:

.. code-block:: python

    >>> dev_raw_data_source.set_attributes(data_format='TEXT',
                                           raw_data='hi\nhello\nhow are you?')

Connecting stages
-----------------

As described above, to connect the output of one stage to the input of
another, simply use the ``>>`` operator between two :py:class:`streamsets.sdk.sdc_models.Stage` instances:

.. code-block:: python

    >>> dev_raw_data_source >> trash

For stages with multiple outputs, simply use ``>>`` multiple times:

.. code-block:: python

    >>> file_tail = builder.add_stage('File Tail')
    >>> file_tail >> trash_1
    >>> file_tail >> trash_2

.. image:: _static/file_tail_to_two_trashes.png

It is also possible to connect the output of one stage to the inputs of multiple
stages, as in the image below:

.. image:: _static/dev_data_generator_to_two_trashes.png

To do this, put the :py:class:`streamsets.sdk.sdc_models.Stage` instances to which you'll be
connecting the same output into a list before using the ``>>`` operator:

.. code-block:: python

    >>> trash_1 = builder.add_stage('Trash')
    >>> trash_2 = builder.add_stage('Trash')
    >>> dev_raw_data_source >> [trash_1, trash_2]


Events
------

To connect the event lane of one stage to another, use the ``>=`` operator:

.. code-block:: python

    >>> dev_data_generator >> trash_1
    >>> dev_data_generator >= trash_2

.. image:: _static/dev_data_generator_with_events.png


Error stages
------------

To add an error stage, use :py:meth:`streamsets.sdk.sdc_models.PipelineBuilder.add_error_stage`:

.. code-block:: python

    >>> discard = builder.add_error_stage('Discard')


Interacting with Pipeline Snapshots
-----------------------------------

Capturing a Snapshot
~~~~~~~~~~~~~~~~~~~~~

Assuming we have an already-stopped pipeline that we'd like to generate a snapshot for, we could use the following
steps to generate a new snapshot:

.. code-block:: python

    >>> # Connect to a DataCollector instance and set the pipeline we wish to generate a snapshot for
    >>> sdc = DataCollector("https://localhost:18630")
    >>> pipeline = sdc.pipelines.get(id='testpipel1c35d2ff-5e49-4f99-ba56-00051fd7845f')
    >>>
    >>> # Capture the snapshot
    >>> snapshot = sdc.capture_snapshot(pipeline, start_pipeline=True, snapshot_name='New Snapshot').snapshot
    >>> snapshot
    <Snapshot (name=New Snapshot, time_stamp=1616718217886, batch_number=1)>

If the pipeline were already-running, ``start_pipeline`` should be set to ``False`` or can be omitted entirely
(default: ``False``).

Reading from a Snapshot
~~~~~~~~~~~~~~~~~~~~~~~

Let's assume the above pipeline consisted of a Dev Data Generator origin writing to Trash destination, with the
origin generating datetime data.

To read output values from a stage we do:

.. code-block:: python

    >>> stage = pipeline.stages[0]
    >>>
    >>> # Read the field attribute from output
    >>> field = snapshot[stage].output[0].field

which gives us a dictionary,

.. code-block:: json

    {'random_value': 2018-11-05 04:31:05.953000}

Now to assert that the value we retrieved is the right value, we do:

.. code-block:: python

    >>> field['random_value'] == datetime.datetime(2018, 11, 5, 4, 31, 5, 953000)

    True

Note that the field value is coerced into the appropriate type, but the underlying raw value is stored along with its
type.

.. code-block:: python

    >>> field['random_value'].raw_value

    1541392265953

    >>> field['random_value'].type

    'DATETIME'

Retrieving an existing Snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Perhaps we had generated a snapshot for the same pipeline previously, either via the DataCollector UI or Python SDK,
and now we'd like to retrieve it. The following would allow us to pick a snapshot based on a number of unique
attributes such as ``'id'``, ``'name'``, or ``'time_stamp'``:

.. code-block:: python

    >>> snapshot = sdc.get_snapshots(pipeline).get(name='Earlier Snapshot')
    >>> snapshot
    <Snapshot (name=Earlier Snapshot, time_stamp=1616716207032, batch_number=1)>
    >>>
    >>> snapshot.id
    'snapshot1616718217454'

Deleting a Snapshot
~~~~~~~~~~~~~~~~~~~

If we've successfully generated a snapshot for a pipeline and no longer need to retain it, it can be deleted using the
:py:meth:`streamsets.sdk.sdc.DataCollector.delete_snapshot` method. The method expects to receive a
:py:class:`streamsets.sdk.sdc_models.Snapshot` instance as an argument, exactly like the one returned by the
:py:meth:`streamsets.sdk.sdc.DataCollector.get_snapshots` method used previously:

.. code-block:: python

    >>> # Check the list of current snapshots for the pipeline
    >>> sdc.get_snapshots(pipeline)
    [<Snapshot (name=New Snapshot, time_stamp=1617379142414, batch_number=1)>, <Snapshot (name=Earlier Snapshot,
    time_stamp=1617379338310, batch_number=1)>]
    >>>
    >>> # Get the snapshot object that corresponds to the snapshot we wish to delete
    >>> snapshot = sdc.get_snapshots(pipeline).get(id='snapshot1617379142318')
    >>> snapshot
    <Snapshot (name=New Snapshot, time_stamp=1617379142414, batch_number=1)>
    >>>
    >>> sdc.delete_snapshot(snapshot)
    <streamsets.sdk.sdc_api.Command object at 0x7f02c29eac88>
    >>>
    >>> # The snapshot has been deleted
    >>> sdc.get_snapshots(pipeline)
    [<Snapshot (name=Earlier Snapshot, time_stamp=1617379338310, batch_number=1)>]

Connecting to Data Collector and Control Hub using signed certificate
---------------------------------------------------------------------

To connect to https enabled Data Collector using a cert file, utilize the attribute
`streamsets.sdk.DataCollector.VERIFY_SSL_CERTIFICATES`:

.. code-block:: python

    >>> from streamsets.sdk import DataCollector
    >>> DataCollector.VERIFY_SSL_CERTIFICATES = '/path/to/certfile'
    >>> sdc = DataCollector('https://localhost:18630')

To skip verifying SSL certifcate:

.. code-block:: python

    >>> from streamsets.sdk import DataCollector
    >>> DataCollector.VERIFY_SSL_CERTIFICATES = False
    >>> sdc = DataCollector('https://localhost:18630')

Similarly, for Control Hub:

.. code-block:: python

    >>> from streamsets.sdk import ControlHub
    >>> ControlHub.VERIFY_SSL_CERTIFICATES = '/path/to/certfile'
    >>> sch = ControlHub('https://localhost:18631', 'username@org', 'password')


Pipeline Labels
---------------

Creating a pipeline with labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> data_collector = sch.data_collectors.get(id=<data_collector_id>)
    >>> pipeline_builder = sch.get_pipeline_builder(data_collector)
    >>> dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    >>> trash = pipeline_builder.add_stage('Trash')
    >>> dev_data_generator >> trash
    >>> labels = ['test/dev', 'test']
    >>> pipeline = pipeline_builder.build(title='Test pipeline with labels', labels=labels)
    >>> sch.publish_pipeline(pipeline)
    >>> pipeline.labels
    [<PipelineLabel (label=test/dev)>,
     <PipelineLabel (label=test)>]

Fetching all pipeline labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   >>> sch.pipeline_labels
   [<PipelineLabel (label=test/dev)>, <PipelineLabel (label=test)>]

To fetch pipeline labels by parent ID,

.. code-block:: python

    >>> sch.pipeline_labels.get_all(parent_id='test:admin')
    [<PipelineLabel (label=test/dev)>]

Updating labels of an existing pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> pipeline = sch.pipelines.get(commit_id=<commit_id>)
    >>> pipeline.add_label('prod/dev', 'prod')
    >>> sch.publish_pipeline(pipeline)
    >>> pipeline.labels
    [<PipelineLabel (label=test/dev)>,
     <PipelineLabel (label=test)>,
     <PipelineLabel (label=prod/dev)>,
     <PipelineLabel (label=prod)>]

Removing existing labels for a pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> pipeline = sch.pipelines.get(commit_id=<commit_id>)
    >>> pipeline.remove_label('test', 'test/dev')
    >>> sch.publish_pipeline(pipeline)
    >>> pipeline.labels
    [<PipelineLabel (label=prod/dev)>,
     <PipelineLabel (label=prod)>]]

Deleting pipeline labels
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> label = sch.pipeline_labels.get(parent_id='test:admin', label='test/dev')
    >>> sch.delete_pipeline_labels(label)


Job Tags
--------

Creating a job with tags
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job_builder = sch.get_job_builder()
    >>> pipeline = sch.pipelines.get(id=<pipeline id>)
    >>> tags = ['test/dev', 'test']
    >>> job = job_builder.build(job_name='Test job with tags', pipeline=pipeline, tags=tags)
    >>> sch.add_job(job)
    >>> job.tags
    [<Tag (tag=test/dev)>,
     <Tag (tag=test)>]

Fetching jobs using job tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> sch.jobs.get_all(job_tag='test:admin')
    [<Job (job_id=93084250-ef6f-4c0a-b6f8-aff54f905739:admin, job_name=Test job with tags)>]

Updating tags of an existing job
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job = sch.job.get(job_id=<job_id>)
    >>> job.add_tag('prod/dev', 'prod')
    >>> sch.update_job(job)
    >>> job.tags
    [<Tag (tag=test/dev)>,
     <Tag (tag=test)>,
     <Tag (tag=prod/dev)>,
     <Tag (tag=prod)>]

Removing existing tags for a job
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job = sch.job.get(job_id=<job_id>)
    >>> job.remove_tag('test', 'test/dev')
    >>> sch.update_job(job)
    >>> job.tags
    [<Tag (tag=prod/dev)>,
     <Tag (tag=prod)>]]


Importing and Exporting Pipelines
---------------------------------

Simple Data Collector to Data Collector Import-Export Operation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To export a Data Collector pipeline to use in the same or a different Data Collector:

.. code-block:: python

    >>> pipeline_json = sdc.export_pipeline(pipeline=sdc.pipelines.get(title='pipeline name'),
                                            include_plain_text_credentials=True)
    >>> with open('./from_sdc_for_sdc.json', 'w') as f:
    >>>     json.dump(pipeline_json, f)

You can import a pipeline from a JSON file into Data Collector in two ways:

1. Import the JSON file into :py:class:`streamsets.sdk.sdc_models.PipelineBuilder` and add the pipeline:

.. code-block:: python

    >>> with open('./from_sdc_for_sdc.json', 'r') as input_file:
    >>>     pipeline_json = json.load(input_file)
    >>>
    >>> sdc_pipeline_builder = sdc.get_pipeline_builder()
    >>> sdc_pipeline_builder.import_pipeline(pipeline=pipeline_json)
    >>> pipeline = sdc_pipeline_builder.build(title='built from imported json file from sdc')
    >>> sdc.add_pipeline(pipeline)

2. Directly import the pipeline:

.. code-block:: python

    >>> pipeline = sdc.import_pipeline(pipeline=pipeline_json)

Exporting pipelines from Data Collector for Control Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To export a Data Collector pipeline to use in Control Hub, specify the optional argument
``include_library_definitions``.

.. code-block:: python

    >>> pipeline_json = sdc.export_pipeline(pipeline=sdc.pipelines.get(title='pipeline name'),
                                            include_library_definitions=True,
                                            include_plain_text_credentials=True)

Similarly, you can export pipelines from Control Hub using :py:meth:`streamsets.sdk.ControlHub.export_pipelines`.

Importing a pipeline into Control Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can import a pipeline from a JSON file into Control Hub in three ways:

1. Import the JSON file into :py:class:`streamsets.sdk.sch_models.PipelineBuilder` and publish the pipeline:

.. code-block::  python

    >>> with open('./exported_from_sdc.json', 'r') as input_file:
    >>>     pipeline_json = json.load(input_file)
    >>>
    >>> sch_pipeline_builder = sch.get_pipeline_builder()
    >>> sch_pipeline_builder.import_pipeline(pipeline=pipeline_json)
    >>> pipeline = sch_pipeline_builder.build(title='Modified using Pipeline Builder')
    >>> sch.publish_pipeline(pipeline)

2. Import a pipeline from JSON and update the existing pipeline in ControlHub:

The existing pipeline is inferred from the metadata in the pipeline json specified.

.. code-block:: python

    >>> with open('./exported_from_sch.json', 'r') as input_file:
    >>>     pipeline_json = json.load(input_file)
    >>>
    >>> sch_pipeline_builder = sch.get_pipeline_builder()
    >>> sch_pipeline_builder.import_pipeline(pipeline=pipeline_json)
    >>> pipeline = sch_pipeline_builder.build(preserve_id=True)
    >>> sch.publish_pipeline(pipeline)

3. Directly import the pipeline:

.. code-block:: python

    >>> pipeline = sch.import_pipeline(pipeline=pipeline_json,
                                       name='Exported from sdc')

Exporting and Importing multiple Pipelines at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To export multiple pipelines from a Data Collector into a zip archive:

.. code-block:: python

    >>> pipelines_zip_data = sdc.export_pipelines(sdc.pipelines, include_library_definitions=True)
    >>> with open('./sdc_exports_for_sch.zip', 'wb') as output_file:
    >>>     output_file.write(pipelines_zip_data)

To import multiple pipelines into ControlHub from a zip archive:

.. code-block:: python

    >>> with open('./sdc_exports_for_sch.zip', 'rb') as input_file:
    >>>     pipelines_zip_data = input_file.read()
    >>> pipelines = sch.import_pipelines_from_archive(pipelines_file=pipelines_zip_data,
                                                      commit_message='Exported as zip from sdc')

Similarly, you could import multiple pipelines into Data Collector by using
:py:meth:`streamsets.sdk.DataCollector.import_pipelines_from_archive`.

Duplicating a Pipeline
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> pipeline = sch.pipelines.get(commit_id='6889df89-7aaa-4e10-9f26-bdf16af4c0db:admin')
    >>> sch.duplicate_pipeline(pipeline, number_of_copies=2)
    [<Pipeline (pipeline_id=2a385de6-156e-4769-be48-3363fea582d1:admin,
                commit_id=9b0bba1f-6b27-4905-98fa-77b7ce5b57da:admin,
                name=dev copy1,
                version=1-DRAFT)>,
     <Pipeline (pipeline_id=12ae8e89-8d83-4315-9239-a64981fcdbf3:admin,
                commit_id=3fccbdf6-fdbd-418b-be7c-7afec4da8078:admin,
                name=dev copy2,
                version=1-DRAFT)>]


Preview and test run
--------------------

Previewing a pipeline
~~~~~~~~~~~~~~~~~~~~~

To preview a Control Hub pipeline, use :py:meth:`streamsets.sdk.sch.run_pipeline_preview`

.. code-block:: python

    >>> authoring_data_collector = sch.data_collectors.get(url='http://localhost:18630')
    >>> pipeline_builder = sch.get_pipeline_builder(data_collector=authoring_data_collector)
    >>> dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    >>> trash = pipeline_builder.add_stage('Trash')
    >>> dev_data_generator >> trash
    >>> pipeline = pipeline_builder.build('Test pipeline')
    >>> sch.publish_pipeline(pipeline)
    >>>
    >>> preview_command = sch.run_pipeline_preview(pipeline)
    >>> preview = preview_command.preview
    >>> preview[dev_data_generator].output
    [<Record (field={'': '5e9c7f3f-b553-4604-b92b-770fc016cd70'})>,
     <Record (field={'': 'af9eeb58-ff4e-4558-923b-29fbbf94ae8d'})>,
     <Record (field={'': '2b83fada-1eff-45af-bf5c-4c811c5bcc89'})>,
     <Record (field={'': 'aa8c5944-4b95-4aec-9fe3-536d8f0d05f4'})>,
     <Record (field={'': 'a37e6d42-87ab-4736-8a72-107210e05267'})>,
     <Record (field={'': 'dfc4f1f5-854c-4c9e-8324-21505412f4f0'})>,
     <Record (field={'': 'cfd42fc9-4399-44ec-8caf-f2e1d31cd36e'})>,
     <Record (field={'': 'd03ff7c6-0a70-438d-aaeb-01736bddaf52'})>,
     <Record (field={'': 'a4077ac0-4a38-4ef8-8914-ac7f34321ecd'})>,
     <Record (field={'': '708067df-f6ea-4fdb-bfb6-e74a1c002bfc'})>]

Test running a pipeline
~~~~~~~~~~~~~~~~~~~~~~~

To test run a Control Hub pipeline, use :py:meth:`streamsets.sdk.sch.test_pipeline_run`

.. code-block:: python

    >>> pipeline = sch.pipelines.get(name='Test pipeline')
    >>> test_run_command = sch.test_pipeline_run(pipeline)
    >>> test_run_command.wait_for_status('RUNNING')
    >>> test_run_command.executor_pipeline
    <Pipeline (id=testRun__48d74ed5-af3c-4196-8696-fba1c6e38673__admin, title=Test pipeline)>
    >>> test_run_command.executor_instance
    <streamsets.sdk.sdc.DataCollector at 0x10e872fd0>
    >>> sch.stop_test_pipeline_run(test_run_command)
    <sdk.sdc_api.StopPipelineCommand at 0x10e4cd050>

Task Scheduler
--------------

Creating a new Scheduled Task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a new Scheduled Task, use :py:meth:`streamsets.sdk.sch.get_scheduled_task_builder` to add a
:py:class:`streamsets.sdk.sch_models.Job` or :py:class:`streamsets.sdk.sch_models.Report` to the task.

.. code-block:: python

    >>> job = sch.jobs[0]
    >>> task = sch.get_scheduled_task_builder().build(task_object=job,
                                                      action='START',
                                                      name='Task for job {}'.format(job.job_name),
                                                      description='Scheduled task for job {}'.format(job.job_name),
                                                      cron_expression='0/1 * 1/1 * ? *',
                                                      time_zone='UTC',
                                                      status='RUNNING')
    >>> sch.publish_scheduled_task(task)

Getting an existing Scheduled Task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> task = sch.scheduled_tasks[0]
    >>> task.runs
    [<ScheduledTaskRun (id=38b82a06-9947-4205-a462-560d7029a182, scheduledTime=1553725200000)>,
     <ScheduledTaskRun (id=b300117e-c339-498b-8393-b8deb69c0f0d, scheduledTime=1553725080000)>,
     <ScheduledTaskRun (id=e7048225-b3d5-4788-9620-c709f24a02aa, scheduledTime=1553725140000)>,
     <ScheduledTaskRun (id=ff1874ac-f0c9-4c72-beec-db397f7b02de, scheduledTime=1553725260000)>]

Operating on an existing Scheduled Task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> task = sch.scheduled_tasks[0]
    >>>
    >>> task.pause()
    <ScheduledTask (id=f63ec318-1ea7-4e99-a0a6-cc68be962ce2, name=Task for job a, status=PAUSED)>
    >>>
    >>> task.kill()
    <ScheduledTask (id=f63ec318-1ea7-4e99-a0a6-cc68be962ce2, name=Task for job a, status=KILLED)>
    >>>
    >>> task.delete()
    <ScheduledTask (id=f63ec318-1ea7-4e99-a0a6-cc68be962ce2, name=Task for job a, status=DELETED)>


Users
-----

Creating a new user
~~~~~~~~~~~~~~~~~~~

You can create a new user using :py:class:`streamsets.sdk.sch_models.UserBuilder`.

.. code-block:: python

    >>> user_builder = sch.get_user_builder()
    >>> user = user_builder.build(id='jonsmith@test',
                                  display_name='jon smith',
                                  email_address='johnsmith@gmail.com')
    >>> user.roles = ['Job Operator', 'Pipeline Editor', 'Organization User']
    >>> sch.add_user(user)

Retrieving existing users
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Get all users belonging to current organization
    >>> sch.users
    [<User (id=admin@test, display_name=admin)>,
     <User (id=jonsmith@test, display_name=jon smith)>]
    >>>
    >>> # Get a particular user
    >>> sch.users.get(id='jonsmith@test')
    <User (id=jonsmith@test, display_name=jon smith)>

Updating an existing user
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> user = sch.users.get(id='jonsmith@test')
    >>> user.roles = ['Organization User']
    >>> sch.update_user(user)

Deactivating existing users
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Deactivate single user
    >>> user = sch.users.get(id='jonsmith@test')
    >>> sch.deactivate_user(user)
    >>>
    >>> # Delete multiple users
    >>> users = sch.users.get_all(display_name='Test User')
    >>> sch.deactivate_user(*users)

Deleting existing users
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Deactivate and delete a single user
    >>> user = sch.users.get(id='jonsmith@test')
    >>> sch.delete_user(user, deactivate=True)
    >>>
    >>> # Delete multiple users
    >>> users = sch.users.get_all(display_name='Test User')
    >>> sch.delete_user(*users)


Groups
------

Creating a new Group
~~~~~~~~~~~~~~~~~~~~

You can create a new Group using :py:class:`streamsets.sdk.sch_models.GroupBuilder`.

.. code-block:: python

    >>> group_builder = sch.get_group_builder()
    >>> group = group_builder.build(id='test@admin', display_name='Test Group')
    >>> group.users = ['admin@admin']
    >>> sch.add_group(group)

Retrieving existing groups
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Get all groups belonging to current organization
    >>> sch.groups
    [<Group (id=all@admin, display_name=all)>,
     <Group (id=test@admin, display_name=Test Group)>]
    >>>
    >>> # Get a particular group
    >>> sch.groups.get(id='test@admin')
    <Group (id=test@admin, display_name=Test Group)>

Updating an existing Group
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> group = sch.groups.get(display_name='Test Group')
    >>> group.users.append('test@admin')
    >>> group.roles.append('Data SLA User')
    >>> group.roles.remove('Data SLA Editor')
    >>> sch.update_group(group)

Deleting existing Groups
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Delete a single group
    >>> group = sch.groups.get(display_name='Test Group')
    >>> sch.delete_group(group)
    >>>
    >>> # Delete multiple groups
    >>> groups = sch.groups.get_all(display_name='Test Group')
    >>> sch.delete_group(*groups)


Event Subscriptions
-------------------

Creating an Event Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> subscription_builder = sch.get_subscription_builder()
    >>>
    >>> subscription_builder.add_event(event_type='Pipeline Committed')
    >>> subscription_builder.set_email_action(recipients=['fake@fake.com'],
                                              subject='{{PIPELINE_NAME}} pipeline was committed',
                                              body=('{{PIPELINE_COMMITTER}} committed the {{PIPELINE_NAME}} pipeline '
                                                    'on {{PIPELINE_COMMIT_TIME}}.'))
    >>> subscription = subscription_builder.build(name='Sample Subscription')
    >>> sch.add_subscription(subscription)

Retrieving a Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> subscription = sch.subscriptions.get(name='Sample Subscription')
    >>> subscription
    <Subscription (id=fbee1816-6c72-40ec-a432-e19b5ccac891:admin, name=manual)>

Getting the Events from a Subscription object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> event = subscription.events.get(event_type='Pipeline Committed')
    >>> event
    <SubscriptionEvent (event_type=Pipeline Committed, filter=)>
    >>> subscription.events
    [<SubscriptionEvent (event_type=Job Status Change, filter=)>,
     <SubscriptionEvent (event_type=Data SLA Triggered, filter=)>,
     <SubscriptionEvent (event_type=Pipeline Committed, filter=)>,
     <SubscriptionEvent (event_type=Pipeline Status Change, filter=)>,
     <SubscriptionEvent (event_type=Report Generated, filter=)>,
     <SubscriptionEvent (event_type=Data Collector not Responding, filter=)>]

Getting the action from a Subscription object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> action = subscription.action
    >>> action
    <SubscriptionAction (event_type=EMAIL)>

Update an existing Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> subscription = sch.subscriptions.get(name='Sample Subscription')
    >>> # Import Subscription into builder
    >>> subscription_builder = sch.get_subscription_builder()
    >>> subscription_builder.import_subscription(subscription)
    >>> # Remove existing event
    >>> subscription_builder.remove_event(event_type='Pipeline Committed')
    >>> # Add a new Job Status Change Event
    >>> subscription_builder.add_event(event_type='Job Status Change', filter="${{JOB_ID=='{}'}}".format(job.job_id))
    >>> # Change action to Webhook action
    >>> subscription_builder.set_webhook_action(uri='https://google.com')
    >>> # Build the subscription
    >>> subscription = subscription_builder.build(name='Sample Subscription updated')
    >>> # Update the Subscription on Control Hub instance
    >>> sch.update_subscription(subscription)

Deleting an existing Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> subscription = sch.subscriptions.get(name='Sample Subscription updated')
    >>> sch.delete_subscription(subscription)

Acknowledging an event subscription error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block: python

    >>> subscription = sch.subscriptions.get(name='Sample Subscription')
    >>> subscription.error_message
    'Failed to trigger email action for event fbee1816-6c72-40ec-a432-e19b5ccac891:admin due to: Issues:
    [APP_ISSUES_01 - Exception: com.streamsets.datacollector.email.EmailException: javax.mail.SendFailedException:
    Invalid Addresses;\n  nested exception is:\n\tcom.sun.mail.smtp.SMTPAddressFailedException: 553 5.1.2
    The recipient address <fake@fake.com> is not a valid RFC-5321 address. x203sm9391603pgx.61 - gsmtp\n]'
    >>>
    >>> sch.acknowledge_event_subscription_error(subscription)
    <sdk.sch_api.Command at 0x111c50eb8>
    >>> subscription.error_message
    None

Retrieving subscription audits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve subscription audits:

.. code-block:: python

    >>> sch.subscription_audits
    [<SubscriptionAudit (subscription_name='pipeline',
                         event_name='PIPELINE_COMMITTED',
                         external_action_type='WEBHOOKV1',
                         created_time=1607548034094)>,
     <SubscriptionAudit (subscription_name='new pipeline',
                         event_name='PIPELINE_COMMITTED',
                         external_action_type='WEBHOOKV1',
                         created_time=1607548034094)>]


Reports
-------

Creating a Report Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Report Definition can be built and added to Control Hub using the
:py:class:`streamsets.sdk.sch_models.ReportDefinitionBuilder`.

.. code-block:: python

    >>> report_definition_builder = sch.get_report_definition_builder()
    >>> # Set the report generation time frame for last 30 minutes.
    >>> report_definition_builder.set_data_retrieval_period(start_time='${time:now() - 30 * MINUTES}',
                                                            end_time='${time:now()}')
    >>>
    >>> # Add resources to the Report.
    >>> job = sch.jobs.get(job_name='name')
    >>> topology = sch.topologies.get(topology_name='name')
    >>> report_definition_builder.add_report_resource(job)
    >>> report_definition_builder.add_report_resource(topology)
    >>>
    >>> # Build and publish.
    >>> report_definition = report_definition_builder.build(name='from sdk')
    >>> sch.add_report_definition(report_definition)

Creating Report Definitions using absolute time range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a report definition for a fixed absolute time range, use the same arguments and methods as above but specify
timestamp in milliseconds as both start_time and end_time.

.. code-block:: python

    >>> import datetime
    >>> start_time = datetime.datetime(2019, 4, 1).timestamp() * 1000
    >>> end_time = datetime.datetime(2019, 4, 10).timestamp() * 1000
    >>> report_definition_builder.set_data_retrieval_period(start_time=start_time,
                                                            end_time=end_time)

Generating a Report
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> report_defintion = sch.report_definitions.get(name='from sdk')
    >>> report_command = report_defintion.generate_report()
    >>>
    >>> report_command.report
    Report is still being generated...
    >>>
    >>> # After the report is generated,
    >>> report_command.report
    <Report (id=13114c45-15ce-44d1-8ff5-bc5ba73f5b8a:admin, name=from sdk at 04-12-2019 18:38:00 UTC)>


Getting existing Report Definitions and Reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Get Report Definitions
    >>> sch.report_definitions.get(name='from sdk')
    <ReportDefinition (id=4c7dccf1-30a8-4b81-9463-7723e0697d62:admin, name=from sdk)>
    >>>
    >>> # Get Report Resources
    >>> sch.report_definitions.get(name='from sdk').report_resources
    [<ReportResource (resource_type=JOB, resource_id=fa9517c8-c93d-432e-b880-9c2d2d1c5dfe:admin)>,
     <ReportResource (resource_type=TOPOLOGY, resource_id=b124dedf-cbc9-4632-a765-8fc59b9636ab:admin)>]
    >>>
    >>> # Get Reports
    >>> sch.report_definitions.get(name='from sdk').reports
    [<Report (id=13114c45-15ce-44d1-8ff5-bc5ba73f5b8a:admin, name=from sdk at 04-12-2019 18:38:00 UTC)>,
     <Report (id=663490aa-b413-460d-8b0d-38b52592cfb2:admin, name=from sdk at 04-12-2019 18:31:00 UTC)>]

Downloading existing Reports as PDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> report_defintion = sch.report_definitions.get(name='from sdk')
    >>> report_content = report_defintion.reports[0].download()
    >>> with open('report.pdf', 'wb') as f:
    >>>     f.write(report_content)

Updating an existing Report Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> report_definition_builder = sch.get_report_definition_builder()
    >>> report_definition = sch.report_definitions.get(name='from sdk')
    >>>
    >>> # Import Report Definition into Report Definition Builder.
    >>> report_definition_builder.import_report_definition(report_definition)
    >>>
    >>> # Remove topology from resources
    >>> topology = sch.topologies[0]
    >>> report_definition_builder.remove_report_resource(topology)
    >>>
    >>> # Add job to resources
    >>> job = sch.jobs.get(job_name='another job')
    >>> report_definition_builder.add_report_resource(job)
    >>>
    >>> # Update time range from last 30 minutes to last 2 days
    >>> report_definition_builder.set_data_retrieval_period(start_time='${time:now() - 2 * DAYS}',
                                                            end_time='${time:now()}')
    >>> sch.update_report_definition(report_defintion)

Scheduling Report generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> report_def = sch.report_definitions[0]
    >>> task = sch.get_scheduled_task_builder().build(task_object=report_def,
                                                      action='START',
                                                      name='Task for Report {}'.format(report_def.name),
                                                      cron_expression='0/1 * 1/1 * ? *',
                                                      time_zone='UTC')
    >>> sch.publish_scheduled_task(task)


Topologies
----------

Retrieving Topologies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> topology = sch.topologies.get(name='Sample Topology')
    >>> topology
    [<Topology (topology_id=ec7e5456-d935-4696-9c0f-01ea3c8e9003:admin, topology_name=dev)>]

Importing Topologies
~~~~~~~~~~~~~~~~~~~~

To import a set of topologies from a compressed archive, use :py:meth:`streamsets.sdk.sch.ControlHub.import_topologies`:

.. code-block:: python

    >>> with open('topologies.zip', 'rb') as topologies_file:
    >>>     topologies = sch.import_topologies(archive=topologies_file)

Exporting Topologies
~~~~~~~~~~~~~~~~~~~~

To export a set of topologies from Control Hub, use :py:meth:`streamsets.sdk.sch.ControlHub.export_topologies`:

.. code-block:: python

    >>> topologie_zip_data = sch.export_topologies(topologies=sch.topologies)
    >>> with open('./sch_topologies_export.zip', 'wb') as output_file:
    >>>     output_file.write(topologies_zip_data)

Deleting Topologies
~~~~~~~~~~~~~~~~~~~

To delete all versions of a topology

.. code-block:: python

    >>> sch.delete_topology(topology)

To delete only the selected version of a topology

.. code-block:: python

    >>> sch.delete_topology(topology, only_selected_version=True)


Retrieving Data SLAs
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> topology = sch.topologies.get(topology_name='Sample Topology')
    >>> topology.data_slas
    [<DataSLA (label='Sample Data SLA', last_modified_on=1607558436834, status='INACTIVE')>]

Adding Data SLAs
~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job = topology.jobs.get(job_id='Example Job in Sample Topology')
    >>> data_sla_builder = sch.get_data_sla_builder()
    >>> data_sla = data_sla_builder.build(topology=topology,
                                          label='Sample Data SLA',
                                          job=job,
                                          alert_text='Sample Alert')
    >>> topology.add_data_sla(data_sla)

Activating Data SLAs
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> data_sla1 = topology.data_slas.get(label='Sample Data SLA')
    >>> data_sla2 = topology.data_slas.get(label='Another Sample Data SLA')
    >>> data_sla3 = topology.data_slas.get(label='A Third Sample Data SLA')
    >>> topology.activate_data_sla(data_sla1, data_sla2, data_sla3)
    <sdk.sch_api.Command at 0x10b3e8a90>

Deactivating Data SLAs
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> topology.deactivate_data_sla(data_sla1, data_sla2)
    <sdk.sch_api.Command at 0x10b3e8a90>

Deleting Data SLAs
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> topology.delete_data_sla(data_sla1, data_sla3)
    <sdk.sch_api.Command at 0x10b3e8a90>


Job Templates
-------------

Creating a Job Template
~~~~~~~~~~~~~~~~~~~~~~~

To create a Job Template, simply pass ``job_template=True`` to :py:meth:`streamsets.sdk.sch_models.JobBuilder.build`:

.. code-block:: python

    >>> job_builder = sch.get_job_builder()
    >>> job_template = job_builder.build('Job Template using SDK',
                                         pipeline=simple_pipeline,
                                         job_template=True,
                                         runtime_parameters={'x': 'y', 'a': 'b'})
    >>> sch.add_job(job_template)

Starting Job Instances using Job Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``instance_name_suffix`` to specify suffix type for the Job instances.

.. code-block:: python

    >>> job_template = sch.jobs.get(name='Job Template using SDK')
    >>> runtime_parameters = [{'x': '1', 'a': 'b'},
                              {'x': '2', 'a': 'b'}]
    >>> jobs = sch.start_job_template(simple_job_template,
                                      instance_name_suffix='PARAM_VALUE',
                                      parameter_name='x',
                                      runtime_parameters=runtime_parameters)

Spawning multiple Job instances using same parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``number_of_instances`` to specify the number of Job instances to be spawned using the specified runtime parameters.

.. code-block:: python

    >>> job_template = sch.jobs.get(name='Job Template using SDK')
    >>> jobs = sch.start_job_template(simple_job_template,
                                      number_of_instances=3)

In this case, since ``runtime_parameters`` is not specified, the default set of parameters specified when creating the
Job Template is used.

Deleting a Job Template
~~~~~~~~~~~~~~~~~~~~~~~

Job Templates can be deleted the same way a regular Job is deleted:

.. code-block:: python

    >> sch.delete_job(job_template)


Jobs
----

Creating a Job
~~~~~~~~~~~~~~

To create a new job, use :py:meth:`streamsets.sdk.sch.get_job_builder`:

.. code-block:: python

    >>> job_builder = sch.get_job_builder()
    >>> pipeline = sch.pipelines[0]
    >>> job = job_builder.build('job name', pipeline=pipeline)
    >>>
    >>> sch.add_job(job)

Creating a Job with a particular pipeline version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job_builder = sch.get_job_builder()
    >>> pipeline = sch.pipelines[0]
    >>> pipeline_commit = pipeline.commits.get(version='1')
    >>> job = job_builder.build('job name', pipeline=pipeline, pipeline_commit=pipeline_commit)
    >>> sch.add_job(job)

Upgrading a Job
~~~~~~~~~~~~~~~

To upgrade one or more jobs to the corresponding latest pipeline version, use :py:meth:`streamsets.sdk.sch.upgrade_job`:

.. code-block:: python

    >>> jobs = sch.jobs.get_all(pipeline_commit_label='v1')
    >>> sch.upgrade_job(*jobs)

Updating a Job with a different pipeline version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job = sch.jobs.get(pipeline_commit_label='v2')
    >>> pipeline = sch.pipelines[0]
    >>> pipeline_commit = pipeline.commits.get(version='1')
    >>> job.commit = pipeline_commit
    >>> sch.update_job(job)

Duplicating a Job
~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job = sch.jobs.get(job_id='6889df89-7aaa-4e10-9f26-bdf16af4c0db:admin')
    >>> sch.duplicate_job(job, number_of_copies=2)
    [<Job (job_id=e52c4157-2aec-4b7c-b875-8244d5dc220b:admin, job_name=Job for dev copy1)>,
     <Job (job_id=c0307b6e-2eee-44e3-b8b1-9600e25a30b7:admin, job_name=Job for dev copy2)>]

Resetting offsets
~~~~~~~~~~~~~~~~~

To reset offsets for one or more jobs use :py:meth:`streamsets.sdk.sch.reset_origin`:

.. code-block:: python

    >>> jobs = sch.jobs
    >>> sch.reset_origin(*jobs)

Uploading offsets
~~~~~~~~~~~~~~~~~

To upload offsets for a job use :py:meth:`streamsets.sdk.sch.upload_offset`:

.. code-block:: python

    >>> job = sch.jobs.get(name='job name')
    >>>
    >>> with open('offset.json') as offset_file:
    >>>     sch.upload_offset(job, offset_file=offset_file)

:py:meth:`streamsets.sdk.sch.upload_offset` can also be used to upload offset as a json:

.. code-block:: python

    >>> offset_json = {"version" : 2,
                       "offsets" : {"$com.streamsets.datacollector.pollsource.offset$" : None}}
    >>> sch.upload_offset(job, offset_json=offset_json)

Retrieving Job Status History
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job = sch.jobs[0]
    >>> job.history
    [<JobStatus (status=INACTIVE, start_time=1585923912290, finish_time=1585923935759, run_count=2)>,
     <JobStatus (status=INACTIVE, start_time=1585923875846, finish_time=1585923897766, run_count=1)>]

Retrieving Run Events from Job History
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> job_status = job.history[0]
    >>> job_status.run_history
    [<JobRunEvent (user=admin@admin, time=1560367534056, status=ACTIVATING)>,
     <JobRunEvent (user=admin@admin, time=1560367540929, status=DEACTIVATING)>,
     <JobRunEvent (user=None, time=1560367537771, status=DEACTIVATING)>,
     <JobRunEvent (user=None, time=1560367537814, status=DEACTIVATING)>]

Retrieving Offsets
~~~~~~~~~~~~~~~~~~

To retrieve current offsets of a job use :py:attr:`streamsets.sdk.sch.Job.current_status`:

.. code-block:: python

   >>> job.current_status.offsets
   [<JobOffset (sdc_id=0501dc93-8634-11e9-99f3-97919257db3c, pipeline_id=896197a7-9639-4575-9784-260f1dc46fbc:admin)>]

To retrieve offsets at a particular job run use :py:attr:`streamsets.sdk.sch.Job.history`:

.. code-block:: python

   >>> # Get the latest run from the job history
   >>> job_status = job.history[0]
   >>> job_status.offsets
   [<JobOffset (sdc_id=0501dc93-8634-11e9-99f3-97919257db3c, pipeline_id=896197a7-9639-4575-9784-260f1dc46fbc:admin)>]

Metrics
~~~~~~~

To access metrics for a job, reference the ``metrics`` attribute of a :py:class:`streamsets.sdk.sch_models.Job` instance.
This will return a :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.JobMetrics`
objects that are in reverse chronological order (newest first):

.. code-block:: python

    >>> job = sch.jobs.get(job_name='job name')
    >>> job.metrics
    [<JobMetrics (run_count=5, input_count=3204, output_count=3204, total_error_count=0)>,
    <JobMetrics (run_count=4, input_count=24740, output_count=24740, total_error_count=0)>,
    <JobMetrics (run_count=3, input_count=9960, output_count=9960, total_error_count=0)>,
    <JobMetrics (run_count=2, input_count=9564, output_count=9564, total_error_count=0)>,
    <JobMetrics (run_count=1, input_count=792, output_count=792, total_error_count=0)>]

We can also reference the ``history`` attribute of a :py:class:`streamsets.sdk.sch_models.Job` instance to figure out
which job run we might be interested in. For example, if we wanted to know which job run executed at
Apr 01 2021 16:39:48 GMT (unix-timestamp '1617295188217') and get the metrics for it, we could use the following steps:

.. code-block:: python

    >>> job.history.get(start_time=1617295188217)
    <JobStatus (status=INACTIVE, start_time=1617295188217, finish_time=1617295209406, run_count=2)>
    >>> # This was run_count 2, so now we know which run_count to reference for this run's metrics
    >>> job.metrics.get(run_count=2)
    <JobMetrics (run_count=2, input_count=9564, output_count=9564, total_error_count=0)>

Historic Time Series Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To access time series metrics for a job use :py:meth:`streamsets.sdk.sch_models.Job.time_series_metrics`:

.. code-block:: python

    >>> job_time_series_metrics = job.time_series_metrics(metric_type='Record Throughput Time Series')
    >>> job_time_series_metrics
    <JobTimeSeriesMetrics (
    input_records=<JobTimeSeriesMetric (name=pipeline_batchInputRecords_meter,
                                        time_series={'2019-06-24T19:35:01.34Z': 182000.0,
                                                     '2019-06-24T19:36:03.273Z': 242000.0,
                                                     '2019-06-24T19:37:05.202Z': 303000.0,
                                                     '2019-06-24T19:38:07.135Z': 363000.0,
                                                     '2019-06-24T19:39:09.065Z': 424000.0})>,
    output_records=<JobTimeSeriesMetric (name=pipeline_batchOutputRecords_meter,
                                         time_series={'2019-06-24T19:35:01.34Z': 182000.0,
                                                      '2019-06-24T19:36:03.273Z': 242000.0,
                                                      '2019-06-24T19:37:05.202Z': 303000.0,
                                                      '2019-06-24T19:38:07.135Z': 363000.0,
                                                      '2019-06-24T19:39:09.065Z': 424000.0})>,
    error_records=<JobTimeSeriesMetric (name=pipeline_batchErrorRecords_meter,
                                        time_series={'2019-06-24T19:35:01.34Z': 0.0,
                                                     '2019-06-24T19:36:03.273Z': 0.0,
                                                     '2019-06-24T19:37:05.202Z': 0.0,
                                                     '2019-06-24T19:38:07.135Z': 0.0,
                                                     '2019-06-24T19:39:09.065Z': 0.0})>)>
    >>> job_time_series_metrics.input_records
    <JobTimeSeriesMetric (name=pipeline_batchInputRecords_meter, time_series={'2019-06-24T19:35:01.34Z': 182000.0,
                                                                              '2019-06-24T19:36:03.273Z': 242000.0,
                                                                              '2019-06-24T19:37:05.202Z': 303000.0,
                                                                              '2019-06-24T19:38:07.135Z': 363000.0,
                                                                              '2019-06-24T19:39:09.065Z': 424000.0})>
    >>> job_time_series_metrics.input_records.time_series
    {'2019-06-24T19:35:01.34Z': 182000.0,
     '2019-06-24T19:36:03.273Z': 242000.0,
     '2019-06-24T19:37:05.202Z': 303000.0,
     '2019-06-24T19:38:07.135Z': 363000.0,
     '2019-06-24T19:39:09.065Z': 424000.0}

Login and Action audits
~~~~~~~~~~~~~~~~~~~~~~~

To retrieve login audits for the current organization:

.. code-block:: python

    >>> sch.login_audits
    [<LoginAudit (user_id=admin@test, ip_address=0:0:0:0:0:0:0:1, login_timestamp=1586455914797, logout_timestamp=0)>,
     <LoginAudit (user_id=admin@test, ip_address=0:0:0:0:0:0:0:1, login_timestamp=1586455135790, logout_timestamp=0)>]

To retrieve action audits for the current organization:

.. code-block:: python

    >>> sch.action_audits
    [<ActionAudit (affected_user_id=admin@test,
                   action=USER_SET_PASSWORD,
                   time=1586385312431,
                   ip_address=0:0:0:0:0:0:0:1)>,
     <ActionAudit (affected_user_id=admin@test,
                   action=GROUP_USER_UPDATE,
                   time=1586385282216,
                   ip_address=0:0:0:0:0:0:0:1)>]

Importing Jobs
~~~~~~~~~~~~~~

To import a set of jobs from a compressed archive, use :py:meth:`streamsets.sdk.sch.ControlHub.import_jobs`:

.. code-block:: python

    >>> with open('jobs.zip', 'rb') as jobs_file:
    >>>     jobs = sch.import_jobs(archive=jobs_file)

Exporting Jobs
~~~~~~~~~~~~~~

To export a set of jobs to a compressed archive, use :py:meth:`streamsets.sdk.sch.ControlHub.export_jobs`:

.. code-block:: python

    >>> jobs = sch.jobs
    >>> jobs_file_data = sch.export_jobs(jobs)
    >>> with open('jobs.zip', 'wb') as jobs_file:
    >>>     jobs_file.write(jobs_file_data)

Balancing Data Collector instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To balance all jobs running on specific Data Collectors, use
:py:meth:`streamsets.sdk.sch.ControlHub.balance_data_collectors`:

.. code-block: python

    >>> data_collectors = sch.data_collectors
    >>> sch.balance_data_collectors(data_collectors)


Pipeline Fragments
------------------

Creating a fragment
~~~~~~~~~~~~~~~~~~~

Creating a fragment is quite similar to creating a pipeline. The only difference is that we specify
``fragment=True`` when initializing Pipeline Builder:

.. code-block:: python

    >>> # Initialize fragment builder
    >>> pipeline_builder = sch.get_pipeline_builder(fragment=True)
    >>>
    >>> # Add stages
    >>> dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    >>> expression_evaluator = pipeline_builder.add_stage('Expression Evaluator')
    >>> field_renamer = pipeline_builder.add_stage('Field Renamer')
    >>>
    >>> # Connect stages
    >>> dev_data_generator >> [expression_evaluator, field_renamer]
    >>>
    >>> # Build and publish pipeline fragment
    >>> fragment = pipeline_builder.build('Test Fragment')
    >>> sch.publish_pipeline(fragment)

.. image:: _static/sample_fragment.png

Retrieving a Pipeline Fragment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve a Pipeline Fragment from a :py:class:`streamsets.sdk.utils.SeekableList` of pipelines, pass
``fragment=True`` when calling :py:meth:`streamsets.sdk.utils.SeekableList.get` or
:py:meth:`streamsets.sdk.utils.SeekableList.get_all`:

.. code-block:: python

    >>> sch.pipelines.get_all(fragment=True)
    [<Pipeline (pipeline_id=88d58863-7e8b-4831-a929-8c56db629483:admin,
                commit_id=600a7709-6a13-4e9b-b4cf-6780f057680a:admin,
                name=Dev as fragment,
                version=1)>,
     <Pipeline (pipeline_id=5b67c7dc-729b-43cc-bee7-072d3feb184b:admin,
                commit_id=491cf010-da8c-4e63-9918-3f5ef3b182f6:admin,
                name=Test Fragment,
                version=1)>]

Using a fragment in a pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add a fragment to a pipeline, use :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.add_fragment`:

.. code-block:: python

    >>> pipeline_builder = sch.get_pipeline_builder()
    >>>
    >>> # Add a fragment
    >>> fragment = sch.pipelines.get(fragment=True, name='Test Fragment')
    >>> fragment_stage = pipeline_builder.add_fragment(fragment)
    >>>
    >>> # Add other stages using add_stage
    >>> trash1 = pipeline_builder.add_stage('Trash')
    >>> trash2 = pipeline_builder.add_stage('Trash')
    >>>
    >>> # Connect stages
    >>> fragment_stage >> trash1
    >>> fragment_stage >> trash2
    >>>
    >>> # Build and publish the pipeline
    >>> pipeline = pipeline_builder.build('Test Pipeline')
    >>> sch.publish_pipeline(pipeline)

.. image:: _static/sample_pipeline_using_fragment.png

Retrieving Pipelines that use a specific Pipeline Fragment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve all the pipelines that use a specific fragment from a :py:class:`streamsets.sdk.utils.SeekableList` of
pipelines, pass ``using_fragment=<fragment>`` when calling :py:meth:`streamsets.sdk.utils.SeekableList.get` or
:py:meth:`streamsets.sdk.utils.SeekableList.get_all`:

.. code-block:: python

    >>> fragment = sch.pipelines.get(fragment=True, name='Test Fragment')
    >>> sch.pipelines.get_all(using_fragment=fragment)
    [<Pipeline (pipeline_id=0e1a42c9-7ce3-4295-84dd-ff53a7b313c3:admin,
                commit_id=f3479d83-6e52-4f85-824c-e8ef4185d8f6:admin,
                name=Test Pipeline,
                version=1)>]

Updating an existing pipeline with new fragment version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update pipelines that use a specific fragment with the new version of fragment, use
:py:meth:`streamsets.sdk.ControlHub.update_pipelines_with_different_fragment_version`:

.. code-block:: python

    >>> fragment = sch.pipelines.get(fragment=True, name='Test Fragment')
    >>> from_fragment_version = fragment.commits.get(version='1')
    >>> to_fragment_version = fragment.commits.get(version='2')
    >>> pipelines = sch.pipelines.get_all(using_fragment=fragment)
    >>> sch.update_pipelines_with_different_fragment_version(pipelines=pipelines,
                                                             from_fragment_version=from_fragment_version,
                                                             to_fragment_version=to_fragment_version)


Provisioning Agents and Deployments
-----------------------------------

Retrieving Provisioning Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Get all provisioning agents belonging to current organization
    >>> sch.provisioning_agents
    [<ProvisioningAgent (id=89A1B2D5-3994-449F-99EB-88CD58958C92, name=minikube-control-agent, type=Kubernetes,
                         version=3.12.0)>]
    >>>
    >>> # Get a particular provisioning agent
    >>> sch.provisioning_agents.get(id='89A1B2D5-3994-449F-99EB-88CD58958C92')
    <ProvisioningAgent (id=89A1B2D5-3994-449F-99EB-88CD58958C92, name=minikube-control-agent, type=Kubernetes,
                        version=3.12.0)>

Deleting Provisioning Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> provisioning_agent = sch.provisioning_agents.get(id='89A1B2D5-3994-449F-99EB-88CD58958C92')
    >>> sch.delete_provisioning_agent(provisioning_agent)

Deactivating and Activating Provisioning Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> sch.deactivate_provisioning_agent(provisioning_agent)
    >>> sch.activate_provisioning_agent(provisioning_agent)

Creating a new Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a new Deployment using :py:class:`streamsets.sdk.sch_models.DeploymentBuilder`.

.. code-block:: python

    >>> deployment_builder = sch.get_deployment_builder()
    >>> provisioning_agent = sch.provisioning_agents[0]
    >>> deployment = deployment_builder.build(name='from sdk',
                                              provisioning_agent=provisioning_agent,
                                              number_of_data_collector_instances=2,
                                              description='from sdk')
    >>> sch.add_deployment(deployment)

You can also create a deployment using a YAML Specification file:

.. code-block:: python

    >>> deployment_builder = sch.get_deployment_builder()
    >>> provisioning_agent = sch.provisioning_agents[0]
    >>> with open('deployment_spec.yaml') as f:
    >>>     deployment_spec = yaml.load(f)
    >>> deployment = deployment_builder.build(name='from sdk with custom spec',
                                              provisioning_agent=provisioning_agent,
                                              number_of_data_collector_instances=1,
                                              description='from sdk',
                                              spec=deployment_spec)
    >>> sch.add_deployment(deployment)

Retrieving existing deployments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> sch.deployments
    [<Deployment (id=329f8688-7458-4d4f-851c-fdfe548411b0:admin, name=from sdk, number_of_data_collector_instances=2, status=INACTIVE)>,
     <Deployment (id=ff1be305-7488-43c6-853f-7829f499082e:admin, name=from sdk with custom spec, number_of_data_collector_instances=1,
                  status=INACTIVE)>]
    >>> provisioning_agent.deployments
    [<Deployment (id=329f8688-7458-4d4f-851c-fdfe548411b0:admin, name=from sdk, number_of_data_collector_instances=2, status=INACTIVE)>,
     <Deployment (id=ff1be305-7488-43c6-853f-7829f499082e:admin, name=from sdk with custom spec, number_of_data_collector_instances=1,
                  status=INACTIVE)>]
    >>> # Get a particular deployment
    >>> sch.deployments.get(id='329f8688-7458-4d4f-851c-fdfe548411b0:admin')
    <Deployment (id=329f8688-7458-4d4f-851c-fdfe548411b0:admin, name=from sdk, number_of_data_collector_instances=2, status=INACTIVE)>

Starting a deployment
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> deployment = sch.deployments.get(id='329f8688-7458-4d4f-851c-fdfe548411b0:admin')
    >>> sch.start_deployment(deployment)

Scaling an active deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> deployment = sch.deployments.get(name='from sdk')
    >>> sch.scale_deployment(deployment, 2)

Stopping a deployment
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from streamsets.sdk.exceptions import DeploymentInactiveError
    >>> try:
    >>>     sch.stop_deployment(deployment)
    >>> except DeploymentInactiveError:
    >>>     sch.acknowledge_deployment_error(deployment)

Updating an existing deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> deployment = sch.deployments.get(name='from sdk')
    >>> deployment.number_of_data_collector_instances = 1
    >>> sch.update_deployment(deployment)

Deleting existing deployments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> # Delete a single deployment
    >>> deployment = sch.deployments.get(name='from sdk')
    >>> sch.delete_deployment(deployment)
    >>>
    >>> # Delete multiple deployments
    >>> deployments = sch.deployments.get_all(number_of_data_collector_instances=1)
    >>> sch.delete_deployment(*deployments)

Registered Data Collectors (Control Hub)
----------------------------------------

Updating Data Collector Resource Thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> data_collector = sch.data_collectors[0]
    >>> data_collector.max_cpu_load
    100.0
    >>> data_collector.max_memory_used
    1000000000000
    >>> data_collector.max_pipelines_running
    1000000000000
    >>> sch.update_data_collector_resource_thresholds(data_collector, max_cpu_load=51.5, max_memory_used=550,
                                                      max_pipelines_running=25)
    >>> data_collector.max_cpu_load
    51.5


Connections
-----------

Creating a new connection
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection_builder = sch.get_connection_builder()
    >>> data_collector = sch.data_collectors.get(url='http://localhost:18630')
    >>> connection = connection_builder.build(title='s3 connection dev',
                                              connection_type='AWS_S3',
                                              authoring_data_collector=data_collector)
    >>> connection.connection_definition.configuration['awsConfig.awsAccessKeyId'] = 123
    >>> connection.connection_definition.configuration['awsConfig.awsSecretAccessKey'] = 456
    >>> sch.add_connection(connection)

Fetching connections
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> sch.connections
    [<Connection (id='25dc5a92-a01c-4fef-979c-824000053396:admin',
     title='s3 connection dev',
     connection_type='AWS_S3')>]

Updating a connection
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection dev')
    >>> connection.connection_definition.configuration['awsConfig.awsAccessKeyId'] = 234
    >>> connection.connection_definition.configuration['awsConfig.awsSecretAccessKey'] = 567
    >>> connection.name = 's3 connection prod'
    >>> sch.update_connection(connection)

Deleting a connection
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> sch.delete_connection(connection)

Using a connection inside a pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> data_collector = sch.data_collectors.get(url='http://localhost:18630')
    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> pipeline_builder = sch.get_pipeline_builder(data_collector)
    >>>
    >>> dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    >>> dev_raw_data_source.stop_after_first_batch = True
    >>> amazon_s3_destination = pipeline_builder.add_stage('Amazon S3', type='destination')
    >>> amazon_s3_destination.set_attributes(bucket='bucket-name',
                                             data_format='JSON')
    >>> dev_raw_data_source >> amazon_s3_destination
    >>>
    >>> amazon_s3_destination.use_connection(connection)
    >>>
    >>> pipeline = pipeline_builder.build('Dev to S3')
    >>> sch.publish_pipeline(pipeline)

Verifying a connection
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> verification_result = sch.verify_connection(connection)
    >>> verification_result
    <ConnectionVerificationResult (status=VALID)>
    >>>
    >>> connection = sch.connections.get(name='s3 connection invalid')
    >>> verification_result = sch.verify_connection(connection)
    >>> verification_result
    <ConnectionVerificationResult (status=INVALID)>
    >>> verification_result.issue_count
    1
    >>> verification_result.issue_message
    'S3_SPOOLDIR_20 - Cannot connect to Amazon S3, reason : com.amazonaws.services.s3.model.AmazonS3Exception:
    The request signature we calculated does not match the signature you provided. Check your key and signing method.'

Get pipelines using a connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> connection.pipeline_commits
    [<PipelineCommit (commit_id=db1e3b87-1499-44ef-93b8-e4e045318c48:admin, version=1, commit_message=None)>]
    >>> connection.pipeline_commits[0].pipeline
    <Pipeline (pipeline_id=5462626e-0243-48dd-8c07-c6787a813e37:admin,
     commit_id=db1e3b87-1499-44ef-93b8-e4e045318c48:admin, name=s3, version=1)>

Retrieving ACL permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> connection.acl
    <ACL (resource_id=cadd8eaa-85f4-48d0-a1a0-ff77a63584cc:admin, resource_type=CONNECTION)>
    >>> connection.acl.permissions
    [<Permission (resource_id=cadd8eaa-85f4-48d0-a1a0-ff77a63584cc:admin, subject_type=USER, subject_id=admin@admin)>]

Adding new permissions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> acl = connection.acl
    >>> actions = ['READ', 'WRITE']
    >>> permission = acl.permission_builder.build(subject_id='testuser@testorg', subject_type='USER', actions=actions)
    >>> acl.add_permission(permission)
    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> connection.acl.permissions.get(subject_id='testuser@testorg')
    <Permission (resource_id=cadd8eaa-85f4-48d0-a1a0-ff77a63584cc:admin, subject_type=USER, subject_id=testuser@testorg)>

Updating existing permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> permission = connection.acl.permissions.get(subject_id='testuser@testorg')
    >>> updated_actions = ['READ']
    >>> permission.actions = updated_actions
    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> connection.acl.permissions.get(subject_id=permission.subject_id).actions
    ['READ']

Removing existing permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection prod')
    >>> permission = connection.acl.permissions.get(subject_id='testuser@testorg')
    >>> connection.acl.remove_permission(permission)

Connection Tags
---------------

Creating a connection with tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection_builder = sch.get_connection_builder()
    >>> data_collector = sch.data_collectors.get(url='http://localhost:18630')
    >>> tags = ['test/dev', 'test']
    >>> connection = connection_builder.build(title='s3 connection dev',
                                              connection_type='AWS_S3',
                                              authoring_data_collector=data_collector,
                                              tags=tags)
    >>> connection.connection_definition.configuration['awsConfig.awsAccessKeyId'] = 123
    >>> connection.connection_definition.configuration['awsConfig.awsSecretAccessKey'] = 456
    >>> sch.add_connection(connection)
    >>> connection.tags
    [<Tag (tag=test/dev)>,
     <Tag (tag=test)>]

Updating tags of an existing connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection dev')
    >>> connection.add_tag('prod/dev', 'prod')
    >>> sch.update_connection(connection)
    >>> connection.tags
    [<Tag (tag=test/dev)>,
     <Tag (tag=test)>,
     <Tag (tag=prod/dev)>,
     <Tag (tag=prod)>]

Removing existing tags for a connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection dev')
    >>> connection.remove_tag('test', 'test/dev')
    >>> sch.update_connection(connection)
    >>> connection.tags
    [<Tag (tag=prod/dev)>,
     <Tag (tag=prod)>]]

Fetching all connection tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   >>> sch.connection_tags
   [<Tag (tag=dev)>, <Tag (tag=prod)>]

To fetch connection tags by parent ID:

.. code-block:: python

   >>> sch.connection_tags.get_all(parent_id='prod:{}'.format(sch.organization))
   [<Tag (tag=prod/data)>, <Tag (tag=prod/pipeline)>]

Connection audits
~~~~~~~~~~~~~~~~~

To retrieve audits for last 30 days:

.. code-block:: python

    >>> sch.connection_audits
    [<ConnectionAudit (user_id=admin@admin,
                       connection_name=s3 connection prod,
                       audit_action=UPDATE,
                       audit_time=1601574060023)>,
     <ConnectionAudit (user_id=admin@admin,
                       connection_name=s3 connection prod,
                       audit_action=CREATE,
                       audit_time=1601574050166)>]

To retrieve audits for a time period:

.. code-block:: python

    >>> import datetime
    >>> current_timestamp = datetime.datetime.now().timestamp() * 1000
    >>> sch.connection_audits.get_all(start_time=0, end_time=current_timestamp)
    [<ConnectionAudit (user_id=admin@admin,
                       connection_name=s3 connection prod,
                       audit_action=UPDATE,
                       audit_time=1601574060023)>,
     <ConnectionAudit (user_id=admin@admin,
                       connection_name=s3 connection prod,
                       audit_action=CREATE,
                       audit_time=1601574050166)>]

To retrieve audits for a given connection:

.. code-block:: python

    >>> connection = sch.connections.get(name='s3 connection invalid')
    >>> sch.connection_audits.get_all(connection=connection)
    [<ConnectionAudit (user_id=admin@admin,
                       connection_name=s3 connection prod,
                       audit_action=UPDATE,
                       audit_time=1601574060023)>,
     <ConnectionAudit (user_id=admin@admin,
                       connection_name=s3 connection prod,
                       audit_action=CREATE,
                       audit_time=1601574050166)>]

To retrieve audits for a different organization:

.. code-block:: python

    >>> sch.connection_audits.get_all(organization='test', start_time=0, end_time=current_timestamp)
    [<ConnectionAudit (user_id=admin@test,
                       connection_name=s3 connection test,
                       audit_action=UPDATE,
                       audit_time=1601574060023)>,
     <ConnectionAudit (user_id=admin@test,
                       connection_name=s3 connection test,
                       audit_action=CREATE,
                       audit_time=1601574050166)>]
