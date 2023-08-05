=======
History
=======

0.6.1 (2021-06-18)
------------------

* Revised output and exception handling.
* Revised code to get rid of code duplicates.
* Small bug fixes.
* Set test_enpt_enmapboxapp_install CI job to 'manual' for now.


0.6.0 (2021-06-16)
------------------

* Added parameters related to three new AC modes in EnPT and ACwater.
* Revised descriptions and titles all over the GUI.
* Revised 'optional' flags.
* Improved connection of the QGIS feedback object to EnPT STDOUT and STDERR stream to fix missing log messages on Linux.
* Updated GUI screenshots and installation.rst.


0.5.0 (2021-06-04)
------------------

* 'make lint' now additionally prints the log outputs.
* Replaced deprecated URLs. Fixed 'make lint'.
* Removed classifiers for Python<=3.5.
* Split  enpt_enmapboxapp.py into separate modules - one on case EnPT is installed externally and
  one in case it is part of the QGIS environment. Added EnPTAlgorithm for the latter case and respective test.
* Adapted new --exclude-patterns parameter of urlchecker.
* The EnPTAlgorithm class now also uses a subcommand to run EnPT to be able to use multiprocessing.
* Updated EnPT entry point.
* Flagged many GUI parameters as 'advanced' to hide them by default.
* Replaced QgsProcessingParameter with QgsProcessingParameterRasterLayer where it makes sense (adds a dropdown menu).
* Avoid crash in case output directory is not set by the user.
* Revised GUI parameters, added dropdown menus.


0.4.7 (2021-01-11)
------------------

* Updated GitLab URLs due to changes on the server side.
* Moved enmap-box, sicor and enpt download from build_enpt_enmapboxapp_testsuite_image.sh to new before_script.sh
  and adjusted 'make gitlab_CI_docker' accordingly.


0.4.6 (2020-12-10)
------------------

* Added URL checker and corresponding CI job.
* Fixed all dead URLs.
* Removed travis related files.


0.4.5 (2020-11-27)
------------------

* Replaced deprecated 'source activate' by 'conda activate'.
* Replaced deprecated add_stylesheet() method by add_css_file() in conf.py.
* Use SPDX license identifier.


0.4.4 (2020-03-26)
------------------

* Replaced deprecated HTTP links.


0.4.3 (2020-03-26)
------------------

* Fixed broken 'pip install enpt_enmapboxapp' on Windows (fixes issue #17).


0.4.2 (2020-03-26)
------------------

* added parameter 'vswir_overlap_algorithm'


0.4.1 (2020-03-26)
------------------

* nosetests are now properly working:
  EnPT is called with the given GUI parameters and sends back a file containing all received parameters
  -> fixes issue #13 (closed)
* fixed Linux implementation
* improved error messages in case not all software components are properly installed


0.4.0 (2020-03-25)
------------------

* EnPT can now be interrupted by pressing the cancel button.
* Replaced placeholder app with a link to start the GUI.
* Added an About-Dialog.
* The package is now publicly available.
* Added PyPI upload.


0.3.0 (2020-01-28)
------------------

* The EnPT output is now properly displayed in the log window during EnPT runtime
* Code improvements
* Some minor documentation improvements


0.2.0 (2020-01-17)
------------------

* The GUI app is now working together with the EnPT backend installed in a separate Anaconda environment.
* Many improvements.
* Added documentation.



0.1.0 (2018-07-05)
------------------

* First release on GitLab.
