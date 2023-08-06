Kolibri Endless Key theme
=========================


How can I install this plugin?
------------------------------

1. Inside your Kolibri virtual environment:
    ``pip install kolibri_endless_key_theme``

2. Activate the plugin and disable the default theme (as only one theme can be active at once):

.. code-block:: sh

  kolibri plugin enable kolibri_endless_key_theme
  kolibri plugin disable default_theme

3. Restart Kolibri.


How can I install this plugin for development?
------------------------------

1. Download this repo.

2. Open a terminal in your Kolibri repo.

3. Run the following commands:

.. code-block:: sh

  pip install -e <LOCAL-PATH-TO-REPO>
  kolibri plugin enable kolibri_endless_key_theme
  kolibri plugin disable default_theme

4. Then run the commands to install frontend packages in Kolibri, this plugin will have its dependencies recursively installed.


How to publish to PyPi?
------------------------------

1. Follow the instructions above to install the plugin for development.

2. From the Kolibri directory run the frontend build command.

3. Update `setup.py` to a newer version.

4. In the terminal move to the root level of repo dir and run the following command to publish to PyPi:

    ``make release``