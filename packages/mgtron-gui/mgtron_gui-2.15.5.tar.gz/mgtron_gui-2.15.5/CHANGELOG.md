# CHANGELOG

Author: Hunter, Christerpher

All notable changes will be appended here.

This file is especially formatted and shall not be edited outside of the format
shown below.
The version number shown in the GUI is pulled directly from this file.

This project, henceforth, will recongnize [semantic versioning](https://semver.org/).

## [⭐.✴️.✳️] - YEAR MONTH DAY

Here we write upgrade and change notes.

⭐ MAJOR version when you make incompatible API changes,

✴️ MINOR version when you add functionality in a backwards compatible manner

✳️ PATCH version when you make backwards compatible bug fixes.

-------------------------------------------------------------------------------

## ✳️ [2.15.4] - 2023 JUNE 12
- Fixed a bug in which non-Teensy devices showed up on the GUI. 

## ✳️ [2.15.3] - 2023 MAY 31
- Corrected Frequency Units header to reflect proper input range.

## ✳️ [2.15.2] - 2023 MAY 24

- Fixed a bug in which user could enter non-letter and non-character inputs
- Power/Bandwidth delineates to 100 or 0 if input is above maximum or below minimum

## ✳️ [2.15.1] - 2023 MAY 19

- Account for no Teensy detected.
- Make a name capital that was previously missed.

## ✴️️ [2.15.0] - 2023 MAY 18

- Add a toggle button to enable/disable auto sending the Mission button.

## ✳️ [2.14.1] - 2023 MAY 16

- Fixed a bug in which user could input power and bandwidth greater than 100 or less than 0.
- Autofill function now delineates all inputs to max of 100 or min of 0.

## ✴️ [2.14.0] - 2023 MAY 16

- Show eight disabled card select buttons on the right side and enable if device is present.

## ✴️ [2.13.0] - 2023 MAY 15

- Change button names to remove word "jam".
- Edited wifi button to show "SCANNING..." on press. 

## ✳️ [2.12.1] - 2023 MAY 10

- Corrected an agregise mispelling of the wifi results functon
- Filled in missing values if the wifi scan returns less than 8 results.

## ✴️ [2.12.0] - 2023 MAY 09

- Change button names and functionality.


## ✳️ [2.11.1] - 2023 APR 24

- No longer reset input power to zero when 'kill all' is pressed.
- Send a trailing newline character to the MGTron when sending commands.
  - This is to ensure that the MGTron stops listening to receive commands.

## ✴️ [2.11.0] - 2023 APR 19

- When selecting a device, the state of the device will be displayed in the GUI.

## ✴️ [2.10.0] - 2023 APR 18

- Right click on the right-side 'card select' button to change the name of the card.

## ✳️ [2.9.1] - 2023 APR 18

- Remove the +/- buttons from all of the input fields.

## ✴️ [2.9.0] - 2023 APR 17

- Power input is now between 0 and 100.

## ✴️ [2.8.0] - 2023 APR 17

- Name a custom save as a mission button will load the custom save into the GUI.

## ✳️ [2.7.1] - 2023 APR 14

- Either choice of picking a device will change the colors accordingly.

## ✴️ [2.7.0] - 2023 APR 14

- The card select buttons on the right side of the GUI automattically turn green if the detected device is equivalent to the serial number provided in the config file.
  
## ✳️[2.6.1] - 2023 APR 13

- Captured all exceptions regarding starting the GUI with zero devices connected.

## ✴️ [2.6.0] - 2023 APR 13

- Right side buttons only appear if a device is connected.
- The refresh button now refreshes the currently selected device.

## ✴️ [2.5.0] - 2023 APR 12

- Can custom save and load configurations in real time

## ✳️[2.4.1] - 2023 APR 12

- Removed the text anomaly in the title bar

## ✴️ [2.4.0] - 2023 APR 11

- Swapped out JSON database for SQLite database

## ✴️[2.3.0] - 2023 FEB 20

- Change the button names to phonetic names
- Added a bluetooth scanning button
- Added bluetooth jamming functionality

## ✴️[2.2.0] - 2023 JAN 05

- Changed the phonetic mission buttons to be more explicit
- Removed the refresh and delete buttons

## ✴️[2.1.1] - 2022 DEC 28

- Make the status inidicators turn grey when a new device is selected

## ✴️[2.1.0] - 2022 DEC 14

- Added state awareness to the GUI
- The power and bandwith state are presented above the input fields

## ⭐[2.0.0] - 2022 DEC 13

- Can select and send commands to any number of MGTrons

## ✴️[1.3.0] - 2022 NOV 29

- Automated the Wifi scanning button.
- Implemented an automatic scan and jam button.

## ✴️[1.2.1] - 2022 NOV 10

- Wifi scan actually sorts by signal strength now.
- Added a getter function to grab the version from this file.

## ✴️[1.2.0] - 2022 NOV 10

- Reset all button only resets power.

## ✴️[1.1.0] - 2022 JUN 17

- Added a custom config file for every quick pick card option

## ⭐[1.0.0] - 2022 JUN 17

- Full save, delete, and select functionality of custom saved configurations

## ✴️[0.13.0] - 2022 JUN 16

- Live update of saved list after deletion
- Added delete and refresh button
- Added live update of load list

## ✴️[0.12.4] - 2022 JUN 16

- Card config file, if it doesnt exist, will auto populate with eigtht spot regardless of devices detected

## ✳️[0.12.3] - 2022 JUN 10

- Automatically overwrite or create save file if file is nonexistant or corrupted
- Mission buttons are configurable via config file location in `_config/`

## ✳️[0.12.2] - 2022 JUN 10

- Custom load functional!
- Reconfigured custom save

## ✳️[0.12.1] - 2022 JUN 7

- Removed the `find_dev.sh` script completely and retained that functionality
- Critical error in `find_dev.sh`; linux device finding listing script
- All phonetic mission buttons are configurable via config files
- Added YAML file to run PyPi update using GitHub Actions

## ✴️[0.12.0] - 2022 JUN 6

- The eight button on the right border correspond to up to eight cards
- Custom save configured and working

## ✴️[0.11.0] - 2022 JUN 3

- Scan and jam wifi automatically in RSSI order
- Added box around mission buttons

## ✳️[0.10.2] - 2022 JUN 3

- Automatically create config file and automatically populate config file
- Remove the word `CONFIG` from the buttons

## ✳️[0.10.1] - 2022 JUN 2

- Corrected multiple device bug
- Created an .ini config file and read contents
- Automatically fill in config if card_1 is not fillied in
- Changed name of all mission buttons
- Added `MISSIONS` above the mission buttons
- Card buttons turn blue if that number of cards are detected, disabled otherwise.

## ✴️[0.10.0] - 2022 JUN 1

- Added a set of buttons along the starboard side of the GUI
- New buttons highlight green when selected and grey when not
- When a device is chosen from the list the list promptly dissapears
- Added graceful exit

## ✳️[0.9.1] - 2022 MAY 31

- Device indicator reads no device detected if no device detected
- Fixed device listing bug
- Optimized scenario for if a single device detected

## ✴️[0.9.0] - 2022 MAY 25

- Now show device location and name
- Turn indicator buttons red if no device detected
- Add loggin to serial calls
- Connected devices are in numerical order

## ✳️[0.8.3] - 2022 MAY 25

- Added version number in bottom right of GUI

## ✳️[0.8.2] - 2022 MAY 24

- GUI will launch with no devices detected

## ✳️[0.8.1] - 2022 MAY 23

- Filling in list that holds all of the devices the GUI can access.

## ✴️[0.8.0] - 2022 MAY 23

- Changelog created.
- Project evolved enough to function and actuate hardware as expected.
