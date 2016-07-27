#!/usr/bin/python
# -*- coding: utf-8 -*-

#Board Default PATHs
DEFAULT_PATH_PREFIX = "/root/test/timesys-test-project"
BOARD_LOG_DIR_PATH = '/tmp/logs/'

#Local Default PATHs
PARAMIKO_LOG = "/tmp/paramiko_log.txt"
LOCAL_LOG_DIR_PATH = '/tmp/logs/'

HOST_CONF = {
              'HOST'      : '192.168.32.27',
              'PORT'      : 22,
              'USER'      : 'root',
              'PASSWORD'  : 'root'
}

SCRIPT_CONF = {
               'TEST_SCRIPT'  : 'target/common/Test.sh',
               'CPU_FREQUENCY': 'target/cpu/test_cpufreq.sh',
               'GPIO_TOGGLE'  : 'target/gpiolib/gpio-toggle.sh',
               'LED_TOGGLE'   : 'target/leds/led-toggle.sh',
               'ADC'          : 'target/hwmon/test_adc.sh',
               'NOR_FLASH'    : 'target/mtd/test_nor.sh',
               'TEST_ADC'     : 'target/hwmon/test_adc.sh',
               'TEST_NAND'    : 'target/mtd/test_nand.sh',
               'PIPELINE'     : 'target/gst-fsl/test_pipelines.sh',
               'BACKLIGHT'    : 'target/backlight/backlight-test.sh',
               'ALTIMETER'    : 'target/iio/test_altimeter.sh',
               'ACCELEROMETER': 'target/iio/test_accelerometer.sh',
               'WLAN'         : 'target/net/test_wlan.sh',
               'MDIO'         : 'target/net/test_mdio.sh',
               'ETH'          : 'target/net/test_eth.sh',
               'EEPROM'       : 'target/eeprom/test_eeprom.sh',
               'PCIE_ENUM'    : 'target/pcie/test_pcie_enumeration.sh',
               'I2C_READ'     : 'target/i2c/i2c_read_verify.sh',
               'I2C_SEND'     : 'target/i2c/i2c_send_command.sh',
               'LINE_TEST'    : 'target/audio/test_line.sh',
               'SPEAKER'      : 'target/audio/test_speaker.sh',
               'MIC_TEST'     : 'target/audio/test_mic.sh',
               'X11_TEST'     : 'target/fb/test_x11.sh',
               'WESTON'       : 'target/fb/test_weston.sh',
               'FS_TEST'      : 'target/fs/test_fs.sh',
               'USBG_M'       : 'target/usb/test_usbg_m_storage.sh',
               'USB_TEST'     : 'target/usb/testusb.sh',
               'USBH_M'       : 'target/usb/test_usbh_m_storage.sh',
               'USBG_M_S'     : 'target/usb/setup_usbg_m_storage.sh',

}

#Parameters for each device corresponding each script
DEV_CONF =  {
           'BBB' :  {
                       'CPU_FREQUENCY': ' 0',
                       'GPIO_TOGGLE'  : ' -v 1',
                       'LED_TOGGLE'   : ' -c 10 -a',
                    },
}
