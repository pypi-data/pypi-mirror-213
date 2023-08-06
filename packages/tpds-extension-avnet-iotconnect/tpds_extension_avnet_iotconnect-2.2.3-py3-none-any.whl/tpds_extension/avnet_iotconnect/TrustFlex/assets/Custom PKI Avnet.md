# Trust Platform Design Suite - Usecase Help - Custom PKI Avnet IoTConnect

This document helps to understand all steps of Usecase transaction diagram.

## Setup requirements
 - [Microchip SAM E54 Curiosity Ultra Development Board](https://www.microchip.com/en-us/development-tool/DM320210)
 - [EBV-IoT Microchip Secure Shield](https://iotconnect.io/ebv/ebv-mchp-secure-solution.html)
 - [EBVchips Heracles 324G Shield](https://www.avnet.com/wps/portal/ebv/products/new-products/npi/2020/ebv-elektronik-heracles-324/)
 - [ST X-NUCLEO-IKS01A2 Sensor Shield](https://www.st.com/en/ecosystems/x-nucleo-iks01a2.html) *(optional)*
 - [MPLAB X IDE](https://www.microchip.com/en-us/development-tools-tools-and-software/mplab-x-ide) 5.45 or above

## Pre Usecase transaction Steps
First start by requesting your **free Avnet IoTConnect cloud account** [here](https://iotconnect.io/ebv/).

 - <span style="color:blue">Make sure EBV-IoT Microchip Secure Shield switch is set to **PROG** position <u>before plugging USB cable</u>.</span>
 - Connect EBV-IoT Microchip Secure Shield USB port to PC running Trust Platform Design Suite v2.
 - Ensure *MPLAB X Path* is set in TPDSv2 menu *File* => *Preference* under *System Settings* as this helps:
    - To program the prototyping kit with factory reset application.
    - To open the embedded project of the Usecase.
 - Note that *~/.trustplatform/spg_avnet_iotconnect* is the **Usecase working directory**. It contains the resources generated during transaction diagram execution.
    - ~ indicates home directory.
        - Windows home directory is \user\username
        - Mac home directory is /users/username
        - Most Linux/Unix home directory is /home/username

## Usecase transaction Steps
**Step 1** requires some information to build the custom PKI for Avnet IoTConnect cloud:

![Step 1 dialog](images/help_dialog1.png)

 - **Organization Name** should typically be set to your company name.
 - **Company ID** is a unique identifier related to your Avnet IoTConnect cloud account:
	- Login to your [Avnet IoTConnect](https://avnet.iotconnect.io/) account.
	- Go to **Settings** tab then select **Company Profile**.

		![Company ID menu](images/help_cpid.png)

	- Locate **CPID** field and click the copy icon ![Copy icon](images/help_copy.png). Paste value in the corresponding Usecase popup.

**Step 2** requires some information to register the root CA certificate to Avnet IoTConnect cloud (only required once per root CA):

![Step 2 dialog](images/help_dialog2.png)

 - **Verification code** can be retrieve from the cloud as following:
	- Login to your [Avnet IoTConnect](https://avnet.iotconnect.io/) account.
		- Go to **Devices** tab then select **Certificates** and click **CA CERTIFICATE** button.
		- Choose a name for your root CA certificate then upload root CA certificate file *root_crt.cer* from Usecase working directory and click **SAVE**.

			![Create CA menu](images/help_createca1.png)

		- The root CA certificate is not yet activated and has *pending* status. Locate **Verification code** and click the copy icon ![Copy icon](images/help_copy.png) then paste it in the corresponding Usecase popup. Press **OK**.

			![Create CA menu](images/help_createca2.png)

		- TPDSv2 has now created a verification root certificate. In the cloud **CA CERTIFICATES** menu, locate your root CA and corresponding **Actions** column and click the upload icon ![Copy icon](images/help_upload.png).
		- Upload verification root certificate *root_verification.cer* from Usecase working directory

After **all** steps are passed, create the device associated resources in Avnet IoTConnect cloud:

 - Register the device template in the cloud as following (only required once per template):
	- Login to your [Avnet IoTConnect](https://avnet.iotconnect.io/) account.
		- Go to **Devices** tab then **Device** and on the left pane click **Templates**.
		- Click **CREATE TEMPLATE** then click **QUICK ADD** button.
		- Browse and select file *EBV-IoT Secure Kit v1.0_template.json* from Usecase working directory and click **SAVE**.

 - Create the new device in the cloud as following:
	- Go to **Devices** tab on the left pane then click **CREATE DEVICE** button:
		- **Unique ID** must be the serial number of the ATECC608. It is displayed in the output view of the Usecase as shown below:

			![Output view](images/help_sn.png)

		- **Display Name** can be any desired name.
		- **Entity** must be your entity name.
		- **Template** must be set to "*EBV-IoT Secure Kit v1.0*".
		- **Certificate** select root CA certificate registered in step 2 and click **SAVE**.

			![Create device menu](images/help_createdev.png)


<span style="color:green">The Avnet IoTConnect cloud setup is complete.</span> ![Checked icon](images/help_check.png)

## Post Usecase transaction Steps
On completing Usecase steps execution on TPDSv2, it is possible to either run the embedded project or view C source files by clicking *MPLAB X Project* or *C Source Folder* button.

- <span style="color:blue">Disconnect EBV-IoT Microchip Secure Shield USB port from PC and set I2C switch to **EXT** position.</span>

- Stack your EBV-IoT Microchip Secure shield, EBV Heracles 324G Shield and ST X-NUCLEO-IKS01A2 Shield *(optional)* on top of your SAME54 Curiosity Ultra Development Board as shown below:

![Avnet IoTConnect Demo Board Stack](images/board_stack.png)

- Plug USB cable to DEBUG USB port of SAME54 Curiosity Development Board then load the Usecase project with MPLAB X IDE:
    - Set the project as Main => right click on Project and select *Set as Main Project*
	- If your MPLAB X Project is located outside TPDSv2, you *must* copy latest generated *cust_def C source and header files* from Usecase working directory to the *certs* folder of your project in Usecase working directory

    - Build and Program the project => right click on Project and select *Make and Program Device*.
	- Log from the embedded project can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1.

<span style="color:green">The device is ready to authenticate with the Avnet IoTConnect cloud.</span> ![Checked icon](images/help_check.png)

## Device Firmware Over-The-Air Update
Going further, it is possible to test the OTA update feature of the Avnet IoTConnect cloud using the following steps:

- MPLAB X Project was configured to generate a binary file after building the sources. Binary file will be located at from Usecase working directory *firmware/same54_heracles_iotconnect_tflxtls.X/dist/default/production* with of size of roughly 330 kB.
- In the **Device** menu of the Avnet IoTConnect backend, click **Firmware** tab then click button **Create Firmware**.
- Choose a firmware **Name** like "SAME54" then select corresponding **Template** and corresponding **Hardware Version**. Enter a **Software Version**, **Hardware Description**, **Software Description** then upload above binary file. Click **Save** button.
- In the firmware **Version** menu, locate the **Draft** column under **Software Upgrades** and click the draft software corresponding to the new board firmware.
- Under **Actions** column click **Test OTA** icon ![Test OTA icon](images/help_testOTA.png) corresponding to the new board firmware to test and deploy.
- A new browser tab opens to allow testing the OTA on a single device only. All fields are pre-selected to avoid deploying a test firmware globally. Choose a test device to update using **Device** dropdown menu. Finally click **Update** button to start the OTA update process.

<span style="color:green">The device can now be updated over-the-air from the Avnet IoTConnect cloud.</span> ![Checked icon](images/help_check.png)

Note: Debugging the project under MPLAB X, requires to disable the after build option to generate the binary file. To do so, open **Project Properties**, expand project **Conf** then select **Building** option. Uncheck **Execute this line after build** to allow project debugging.
