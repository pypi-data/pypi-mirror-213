==========
mosaik-fmi
==========

This mosaik-fmi adapter allows to couple FMUs, which are based on the FMI standard (https://fmi-standard.org) with mosaik.

Installation
============

* mosaik-fmi is based on the FMI++ library, which can be found at https://fmipp.sourceforge.io/
* The FMI++ python interface is used, which can be found at https://github.com/AIT-IES/py-fmipp. See this page also for details about installation and requirements of the python interface.

Test
====

The FMUs for the test is based on https://github.com/modelica/Reference-FMUs.

How to Use
==========
Specify simulator configurations within your scenario script::

    sim_config = {
        'FMI': {
            'python': 'mosaik_fmi.mosaik_fmi:FmuAdapter',
        },
        ...
    }

Initialize the FMU Simulator::

    fmu_sim = world.start('FMI',
                        integrator='integratorCK',
                        work_dir='path/to/the/fmu/directory',
                        fmu_name='FMU_name',
                        fmi_version='2',
                        fmi_type='cs',
                        logging_on=False,
                        instance_name='FMU_name',
                        step_size=60*60)

Instantiate FMU model entity::

    fmu_entity = fmu_sim.FMU_name.create(1,
                                 input_1=1.0,          #  FMU input variable
                                 input_2=2.0,          #  All variables are listed in modelDescription.xml
                                 ...
                                 )

Connect FMU output to another simulator's input::

    world.connect(fmu_entity[0], other_simulator,'fmu_output_1', 'simulator_input_1')

Selecting integrator

Refer to https://fmipp.readthedocs.io/projects/py-fmipp/en/latest/getting-started/model-exchange.html#classes-fmumodelexchangev1-and-fmumodelexchangev2 for choosing different integration algorithms


Getting help
============

If you need help, please visit the `mosaik-users mailing list`__ .

__ https://mosaik.offis.de/mailinglist
