/*
 * roxi_api_wdk.h
 *
 *  Created on: 15. 2. 2021
 *      Author: franekt
 */

#ifndef SOURCEDLL_ROXI_API_WDK_H_
#define SOURCEDLL_ROXI_API_WDK_H_

#include <stdint.h>

#if _WIN32
#	define TYPEDEF_FUNC_PREFIX	__stdcall
#	define API_FUNC_PREFIX		__declspec(dllexport)
#endif /*_WIN32*/

#if __linux__
#	define TYPEDEF_FUNC_PREFIX	/*No Prefix*/
#	define API_FUNC_PREFIX		__attribute__((visibility ("default")))
#endif /*__linux__*/

/**
 *	ROXI API WDK
 *
 *	Is API for configure, test and update SENTIO system
 *
 *	It contains these function groups:
 *
 *	- Connection to Sentio system
 *
 *		- roxi_api_wdk_connect_ccu_via_bus
 *		- roxi_api_wdk_connect_ccu_via_ytun
 *		- roxi_api_wdk_disconnect
 *
 *	- Read and write values
 *
 *		- roxi_api_wdk_read_single_value
 *		- roxi_api_wdk_write_single_value
 *		- roxi_api_wdk_read_all_values_into_json
 *		- roxi_api_wdk_write_values_from_json
 *
 *	- Automated configurations
 *
 *		- roxi_api_wdk_change_profile
 *		- roxi_api_wdk_enroll_peripheral
 *
 *	- Test
 *
 *		- roxi_api_wdk_get_temperature_sensors_info
 *		- roxi_api_wdk_test_servo_position
 *		- roxi_api_wdk_test_pump_relay
 *		- roxi_api_wdk_test_voltage_free_relays
 *		- roxi_api_wdk_get_thermoactuator_info
 *		- roxi_api_wdk_get_room_hc_info
 *		- roxi_api_wdk_get_hcc_itc_supplier
 *		- roxi_api_wdk_get_itc_outdoor_temp
 *
 *	- Update system
 *
 *		- roxi_api_wdk_update_via_autoupdate
 *		- roxi_api_wdk_update_via_autoupdate_end
 *		- roxi_api_wdk_update_via_autoupdate_ok
 *		- roxi_api_wdk_update_via_autoupdate_cancel
 *		- roxi_api_wdk_direct_update_get_device_list
 *		- roxi_api_wdk_direct_update_update_device
 */

/**
 * Basic usage
 *
 *	1) Connect to CCU:
 *		- Call roxi_api_wdk_connect_ccu_via_XXX function.
 *		- Wait until callback function returns RAPI_WDK_STATUS_READY status.
 *
 *	2) Use any function from other function group:
 *		- At same time can run only one function.
 *		- Wait for result status e.g. rwwvfjtcSUCCESS.
 *		- Now any other function can be used.
 *		- Pointer values, that are returned by callback erases after callback function finishes. Copy them or process in callback function.
 *		- Do not call next function before callback of previous function returns.
 *
 *	3) When all is done disconnect from CCU:
 *		- Call roxi_api_wdk_disconnect function
 */

/**
 * Note: best works with CCU with fw 11.b38 or 10.6
 */

/**
 * CONNECTION TO SENTIO SYSTEM
 */

enum rapi_wdk_status
{
	/**
	 * RAPI_WDK_STATUS_FINDING_SERVER
	 * 	- Finding Ytun server where CCU is connected
	 */
	RAPI_WDK_STATUS_FINDING_SERVER,

	/**
	 * RAPI_WDK_STATUS_485BUS_CONNECTING
	 *	- Status description
	 *		Finding and validating USB-200 on running roxi network
	 *	- Troubleshooting:
	 *		Check if PC is connected to CCU via USB-200
	 *	- Details:
	 *		waits in state until roxi bus network is not found
	 */

	RAPI_WDK_STATUS_485BUS_CONNECTING,

	/**
	 * RAPI_WDK_STATUS_YTUN_CONNECTING_SERVER
	 *   - Status description
	 * 	   - Connecting to ytun server
	 *	 - Troubleshooting:
	 *	   - Check if your PC is connected to the Internet
	 *	   - Try it later (server is down)
	 */
	RAPI_WDK_STATUS_YTUN_CONNECTING_SERVER,

	/**
	 * RAPI_WDK_STATUS_YTUN_CONNECTING_DEVICE
	 *   - Status description
	 * 	   - Connecting to device
	 *	 - Troubleshooting:
	 *	   - Check if device is connected to the cloud (Network LED is "solid green")
	 */
	RAPI_WDK_STATUS_YTUN_CONNECTING_DEVICE,

	/**
	 * RAPI_WDK_STATUS_YTUN_AUTHENTICATING
	 *   - Status description
	 * 	   - Verifying service key
	 */
	RAPI_WDK_STATUS_YTUN_AUTHENTICATING,

	/**
	 * RAPI_WDK_STATUS_YTUN_BAD_KEY
	 *   - Status description
	 *    - Bad service password
	 *   - Troubleshooting
	 *    - Try connect again with correct service key
	 */
	RAPI_WDK_STATUS_YTUN_BAD_KEY,

	/**
	 * RAPI_WDK_STATUS_OPENING_ROXI_SESSION
	 *   - Status description
	 *    - Session on roxi is being establish
	 */
	RAPI_WDK_STATUS_OPENING_ROXI_SESSION,

	/**
	 * RAPI_SES_STATUS_READY
	 *   - Status description
	 *    - CCU is successfully connected, now you can use any function to work with.
	 */
	RAPI_WDK_STATUS_READY,

	/**
	 * RAPI_WDK_STATUS_FAULT_BOOTLOADER
	 *   - Status description
	 *    - Device is in bootloader
	 *   - Troubleshooting
	 *    - Try update CCU
	 */
	RAPI_WDK_STATUS_FAULT_BOOTLOADER,

	/**
	 * RAPI_WDK_STATUS_FAULT_GENERAL
	 *   - Status description
	 *    - ROXi network fault has happened (e.g. incompatible protocol)
	 *    - Or another unexpected failure
	 */
	RAPI_WDK_STATUS_FAULT_GENERAL,

	/**
	 * RAPI_WDK_STATUSS_CLOSED
	 *  - Status description
	 *   - Connection with CCU is closed.
	 */
	RAPI_WDK_STATUS_CLOSED,

	/**
	 * RAPI_WDK_STATUS_YTUN_KEY_REVOKED
	 *
	 *   - CCU rejected connection by this key type.
	 *   - CCU not allows connection at all. Key not exists or expired.
	 *   - Troubleshooting
	 *    - Set service/temporary password on CCU
	 */
	RAPI_WDK_STATUS_YTUN_KEY_REVOKED,
};

/**
 * rapi_wdk_status_callback
 *
 * It informs about current connection state
 * It is called every state change
 *
 * Output:
 *  status: described in enum rapi_wdk_status
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_status_callback)(enum rapi_wdk_status status);

/**
 * roxi_api_wdk_connect_ccu_via_bus
 *
 * It creates connection to CCU via USB-200
 *
 * Input:
 *  connection_status_callback
 *
 * Return:
 *  0: connection sequence successfully started
 *  -1: on fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_connect_ccu_via_bus(rapi_wdk_status_callback connection_status_callback);

/**
 * roxi_api_wdk_connect_ccu_via_ytun
 *
 * It creates connection to CCU via Ytun server
 *
 * Input:
 *  connection_status_callback
 *  ccu_reg_key: registration key of CCU ("XXXXX-XXXXX-XXXX")
 *  service_password: Service password
 *
 * Return:
 *  0: connection sequence successfully started
 *  -1: on fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_connect_ccu_via_ytun(rapi_wdk_status_callback			connection_status_callback,
															char								*ccu_reg_key,
															char								*service_password);

/**
 * roxi_api_wdk_disconnect
 *
 * It disconnects current connection to CCU
 *
 * Return:
 * 0: on success
 * -1 on fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_disconnect(void);

/**
 * READ AND WRITE VALUES
 *
 */

enum rapi_wdk_read_single_value_result
{
	rwrsvrSUCCESS,			// Value successfully read
	rwrsvrFAIL,				// Some error occurred
	rwrsvrVALUE_NOT_FOUND,	// Value not found
};

enum rapi_wdk_datatype
{
//																Invalid value
    rwdD1 = 9,	// 1B signed									0x7F
    rwdD2,		// 2B signed									0x7FFF
    rwdD4,		// 4B signed									0x7FFFFFFF
    rwdU1,		// 1B unsigned									0xFF
    rwdU2,		// 2B unsigned									0xFFFF
    rwdU4,		// 4B unsigned									0xFFFFFFFF
    rwdTEXT,	// max 256B										size = 0xFFFF
    rwdDATA,	// max 256B										size = 0xFFFF
    rwdD2_FP10,	// 2B signed fixed point 1 decimal places		0x7FFF
    rwdD2_FP100,// 2B signed fixed point 2 decimal places		0x7FFF
    rwdU2_FP10,	// 2B unsigned fixed point 1 decimal places		0xFFFF
    rwdU2_FP100,// 2B unsigned fixed point 2 decimal places		0xFFFF
};

/**
 * rapi_wdk_read_single_value_callback
 *
 * It gives requested value
 *
 * output:
 *  result: described in enum rapi_wdk_read_single_value_result
 *  oid: value oid
 *  vid: value vid
 *  val_type: value data type, described in enum rapi_wdk_datatype
 *  val_data: pointer to value
 *  val_data_size: size of value
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_read_single_value_callback)(enum rapi_wdk_read_single_value_result result, uint32_t oid, uint16_t vid, enum rapi_wdk_datatype val_type, void *val_data, unsigned val_data_size);

/**
 * roxi_api_wdk_read_single_value
 *
 * It reads single value from CCU
 * This function works with ccu version 10.6 or 11.b36 and higher
 *
 * Input:
 *  read_single_value_callback: described in rapi_wdk_read_single_value_callback
 *  oid: OID of requested value
 *  vid: VID of requested value
 *
 * Return:
 *  0: wait for callback result
 *  -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_read_single_value(rapi_wdk_read_single_value_callback read_single_value_callback, uint32_t oid, uint16_t vid);


enum rapi_wdk_write_single_value_result
{
	rwwsvrSUCCESS,						// Value is successfully written
	rwwsvrVALUE_VALIDATION_NOT_PASS,	// Value is not match limits given by *.csv file
	rwwsvrFAIL,							// Some fail occurred
};

/**
 * rapi_wdk_write_single_value_callback
 *
 * It gives result of single value write
 *
 * Output:
 *  result: described in enum rapi_wdk_write_single_value_result
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_write_single_value_callback)(enum rapi_wdk_write_single_value_result result);

/**
 * roxi_api_wdk_write_single_value
 *
 * It writes single value into CCU
 *
 * Input:
 *  write_single_value_callback: described in rapi_wdk_write_single_value_callback;
 *  oid: Output value OID
 *  vid: Output value VID
 *  data_type: output value data type
 *  data_size: output value data size
 *  data: pointer to output value
 *
 * Optional input:
 *  csv_file_path: Path to validation *.csv file
 *
 * Return:
 *  0: wait for callback result
 *  -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_write_single_value(rapi_wdk_write_single_value_callback write_single_value_callback, uint32_t oid, uint16_t vid, enum rapi_wdk_datatype data_type, uint32_t data_size, void* data, const char *csv_file_path);


enum rapi_wdk_read_all_values_result
{
	rwravrSUCCESS,	// Read all values done
	rwravrFAIL,		// Some error occurred
};

/**
 * rapi_wdk_read_all_values_into_json_callback
 *
 * It gives result of reading all data
 *
 * Output:
 *  result: described in enum rapi_wdk_read_all_values_result
 *  output_json_string: JSON string with all big table values from CCU
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_read_all_values_into_json_callback)(enum rapi_wdk_read_all_values_result result, char *output_json_string);

/**
 * roxi_api_wdk_read_all_values_into_json
 *
 * It reads all big table values from CCU to structured JSON string
 *
 * Input:
 *  read_all_values_into_json_callback: descibed in rapi_wdk_read_all_values_into_json_callback
 *
 * Optional Input:
 *  csv_path: path to *csv file. It is used to add name to each name in JSON structure
 *
 * Return:
 *  0: wait for callback result
 *  -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_read_all_values_into_json(rapi_wdk_read_all_values_into_json_callback read_all_values_into_json_callback, const char *csv_path);


enum rapi_wdk_write_values_from_json_to_ccu
{
	rwwvfjtcSUCCESS,				// All values successfully written
	rwwvfjtcFAIL,					// Some error occurred
	rwwvfjtcVALIDATION_NOT_PASS,	// Some value is not match limits given by *.csv file. OID and VID of that value are in callback parameters
};

/**
 * rapi_wdk_write_values_from_json_callback
 *
 *	It gives result of writing all data
 *
 *	Output:
 *	 result: described in enum rapi_wdk_write_values_from_json_to_ccu
 *	 oid: OID of value that not pass validation
 *	 vid: VID of value that not pass validation
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_write_values_from_json_callback)(enum rapi_wdk_write_values_from_json_to_ccu result, uint32_t oid, uint16_t vid);

/**
 * roxi_api_wdk_write_values_from_json
 *
 * It writes all values from JSON structured string into CCU storage.
 * WARNING: It can't be used for restoring configuration.
 *          CCU by writing into some VIDs runs internal mechanisms that can overwrite restored values.
 *          Or run routines that restarts CCU for example.
 *          By writing all loaded values CCU can behaves unpredictable.
 *          This function can be used for writing selected sequence of VIDs where user knows what he is doing.
 *          E.g. Set desired temperature in all rooms.
 *
 * Input:
 *  callback: described in rapi_wdk_write_values_from_json_callback
 *  input_json_string: JSON structured string with values
 *
 * Optional input:
 *  csv_path: path to csv file. It is used for values validation.
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_write_values_from_json(rapi_wdk_write_values_from_json_callback callback, const char *input_json_string, const char *csv_path);

/**
 * AUTOMATED CONFIGURATION
 */

enum rapi_wdk_change_profile
{
	// End statuses
	rwcpSUCCESS,		// Profile is successfully changed
	rwcpFAIL,			// Some error occurred

	// Progress statuses
	rwcpREBOOTING_CCU,	// CCU is now rebooting. Wait for result. Timestamp of estimated reboot finish is given in reboot_time parameter
};

// Requested profile
enum rapi_wdk_profile
{
	rwpPROFILE_1_0_DISTRICT_HEATING = 0,
	rwpPROFILE_1_0_1_DISTRICT_HEATING_WITH_DHW = 12,
	rwpPROFILE_1_1_BOILER_ORHEAT_PUMP_ON_OFF = 1,
	rwpPROFILE_1_1_1_BOILER_OR_HEAT_PUMP_ON_OFF_WITH_DHW = 13,
	rwpPROFILE_1_2_CONDENSING_BOILER_0_10V = 2,
	rwpPROFILE_1_3_1_DISTRICT_HEATING_1_ITC = 3,
	rwpPROFILE_1_3_2_DISCTRICT_HEATING_2_ITCS = 4,
	rwpPROFILE_1_9_DISTRICT_HEATING_1_ITC_DHW_TANK = 14,
	rwpPROFILE_2_1_0_DISTRICT_HEATING_2_SERIAL_ITCS = 15,
	rwpPROFILE_2_2_1_CONDENSING_BOILER_1_ITC = 6,
	rwpPROFILE_2_2_2_CONDENSING_BOILER_2_ITCS = 11,
	rwpPROFILE_3_3_0_HEAT_PUMP_WITH_MANUAL_HC_CHANGE_OVER = 7,
	rwpPROFILE_3_3_1_HEAT_PUMP_WITH_AUTOMATIC_HC_CHANGE_OVER = 8,
	rwpPROFILE_3_3_2_HEAT_PUMP_1_ITC_MANUAL_HC_CHANGE_OVER = 9,
	rwpPROFILE_3_3_3_HEAT_PUMP_1_ITC_AUTOMATIC_HC_CHANGE_OVER = 10,
	rwpPROFILE_4_1_1_DEHUMIDIFIER_ANY_SOURCE_2_HCC_MANUAL_HC_CHANGE_OVER = 16,
	rwpPROFILE_4_1_2_DEHUMIDIFIER_ANY_SOURCE_1_ITC_MANUAL_HC_CHANGE_OVER = 19,
	rwpPROFILE_4_1_3_DEHUMIDIFIER_ANY_SOURCE_1_ITC_1_HCC_MANUAL_HC_CHANGE_OVER = 18,
	rwpPROFILE_4_1_4_DEHUMIDIFIER_ANY_SOURCE_2_ITC_1_HCC_MANUAL_HC_CHANGE_OVER = 17,
};

/**
 * rapi_wdk_change_profile_callback
 *
 * It gives result of change profile
 *
 * Output:
 *  result: described in enum rapi_wdk_change_profile
 *  reboot time: timestap of CCU reboot finish
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_change_profile_callback)(enum rapi_wdk_change_profile result, uint32_t reboot_time);

/**
 * roxi_api_wdk_change_profile
 *
 * It changes hardware profile
 * This function works with ccu version 10.6 or 11.b36 and higher
 *
 * Input:
 *  callback: described in rapi_wdk_change_profile_callback
 *  profile: requested profile
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_change_profile(rapi_wdk_change_profile_callback callback, enum rapi_wdk_profile profile);


enum rapi_wdk_enroll_peripheral
{
	rwepSUCCESS,	// Peripheral is successfully enrolled
	rwepFAIL,		// Some error occurred
};

enum rapi_wdk_room
{
	rwrGLOBAL,
	rwrROOM_1,
	rwrROOM_2,
	rwrROOM_3,
	rwrROOM_4,
	rwrROOM_5,
	rwrROOM_6,
	rwrROOM_7,
	rwrROOM_8,
	rwrROOM_9,
	rwrROOM_10,
	rwrROOM_11,
	rwrROOM_12,
	rwrROOM_13,
	rwrROOM_14,
	rwrROOM_15,
	rwrROOM_16,
	rwrROOM_17,
	rwrROOM_18,
	rwrROOM_19,
	rwrROOM_20,
	rwrROOM_21,
	rwrROOM_22,
	rwrROOM_23,
	rwrROOM_24,
};

/**
 * rapi_wdk_enroll_peripheral_callback
 *
 * It gives result of peripheral enroll
 *
 * Output:
 *  result: described in enum rapi_wdk_enroll_peripheral
 */
typedef void (TYPEDEF_FUNC_PREFIX *rapi_wdk_enroll_peripheral_callback)(enum rapi_wdk_enroll_peripheral result);

/**
 * It enrolls peripheral into Sentio system
 *
 * Input:
 *  callback: described in rapi_wdk_enroll_peripheral_callback
 *  serial_number: serial number of peripheral "153X-XX-XXXX-XXXX"
 *  room: requested room destination
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_enroll_peripheral(rapi_wdk_enroll_peripheral_callback callback, const char *serial_number, enum rapi_wdk_room room);

/*
 * TEST
 */

enum rapi_wdk_get_temperature_sensors_info
{
	rwgtsiSUCCESS,	// Information about temperature sensors successfully got
	rwgtsiFAIL,		// Some error occurred
};

enum rapi_wdk_connection_status
{
	rwcsCONNECTED_AND_SYNCHRONIZED,		// Peripheral normally runs, values are actual
	rwcsCONNECTED_AND_IN_BOOTLADER,		// Peripheral is in bootloader, values are not actual, device is updating or update fails
	rwcsCONNECTED_AND_NOT_SYNCHRONIZED,	// Peripheral just synchronizing, values are not actual
	rwcsCONNECTED_AND_IN_SERVICE_MODE,	// Peripheral is in service mode values are not actual
	rwcsDISCONNECTED,					// Peripheral is disconnected/lost values are not actual
};

struct rapi_wdk_temperature_sensors_info
{
	char							serial_number[18];	// Serial number of temperature sensor
	enum rapi_wdk_connection_status	connection_status;	// Described in enum rapi_wdk_connection_status
	int16_t							air_temperature;	// Sensor air temperature, invalid value == sensor is not synchronized, has not air temp sensor or is broken
	int16_t							floor_temperature;	// Sensor floor temperature, invalid value == sensor is not synchronized, has not floor temp sensor or is broken
	int16_t							outdoor_temperature;// Sensor outdoor temperature, invalid value == sensor is not synchronized, has not outdoor temp sensor or is broken
};

/**
 * roxi_api_wdk_get_temperature_sensors_callback
 *
 * It gives result of temperature sensors
 *
 * Output:
 *  result: described in enum rapi_wdk_get_temperature_sensors_info
 *  sensors_info: array of sensors, item is described in struct rapi_wdk_temperature_sensors_info
 *  sensors_count: count of sensors
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_get_temperature_sensors_callback)(enum rapi_wdk_get_temperature_sensors_info	result,
																		struct rapi_wdk_temperature_sensors_info	*sensors_info,
																		uint8_t										sensors_count);

/**
 * roxi_api_wdk_get_temperature_sensors_info
 *
 * It loads information of all temperature sensors
 *
 * Input:
 *  callback: described in roxi_api_wdk_get_temperature_sensors_callback
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_get_temperature_sensors_info(roxi_api_wdk_get_temperature_sensors_callback callback);


enum rapi_wdk_test_servo_position
{
	rwspSUCCESS,			// Servo position successfully set
	rwspSERVO_NOT_EXISTS,	// Servo given by servo_number not exists
	rwspFAIL,				// Some error occured
};

enum rapi_wdk_servo_number
{
	rwsnSERVO_1,	// Servo 1
	rwsnSERVO_2,	// Servo 2
};

// Servo position preset when 3 point type is selected
enum rapi_wdk_servo_position
{
	rwspCLOSE	= -10000,
	rwspSTOP	= 0,
	rwspOPEN	= 10000
};

/**
 * roxi_api_wdk_test_servo_position_callback
 *
 * It gives result of servo test
 *
 * Output:
 *  result: described in enum rapi_wdk_test_servo_position
 */

typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_test_servo_position_callback)(enum rapi_wdk_test_servo_position result);


/**
 * roxi_api_wdk_test_servo_position
 *
 * It sets servo position to requested position for given time
 *
 * Input:
 *  callback: described in roxi_api_wdk_test_servo_position_callback
 *  servo_number: select servo number from enum rapi_wdk_servo_numbers
 *  position: set servo position. You can choose preset from enum rapi_wdk_servo_position when servo is set to 3 point type.
 *            Analog type can be set from 0 to 10000
 *  test_time_s: test value duration time in seconds. After this time servo is set to previous position
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_test_servo_position(roxi_api_wdk_test_servo_position_callback callback,
															enum rapi_wdk_servo_number servo_number,
															int16_t position,
															uint16_t test_time_s);


enum rapi_wdk_test_pump_relay
{
	rwtprSUCCESS,			// Pump relay position is successfully set
	rwtprPUMP_NOT_EXISTS,	// Pump relay is not exists in system
	rwtprFAIL,				// Some error occured
};

enum rapi_wdk_pump_number
{
	rwpnPUMP_1,	// Pump relay 1
	rwpnPUMP_2, // Pump rely 2
};

enum rapi_wdk_pump_position
{
	rwppON,	// ON
	rwppOFF	// OFF
};

/**
 * roxi_api_wdk_test_pump_relay_callback
 *
 * It gives result of pump relay test
 *
 * Output:
 *  result: described in enum rapi_wdk_test_pump_relay
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_test_pump_relay_callback)(enum rapi_wdk_test_pump_relay result);

/**
 * roxi_api_wdk_test_pump_relay
 *
 * It sets pump relay position to given value for given time duration
 *
 * Input:
 *  callback: described in roxi_api_wdk_test_pump_relay_callback
 *  pump_number: pump number, described in enum rapi_wdk_pump_number
 *  position: requested pump state, described in enum rapi_wdk_pump_position
 *  test_time_s: after this time in seconds pump returns into previous state
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_test_pump_relay(roxi_api_wdk_test_pump_relay_callback callback,
															enum rapi_wdk_pump_number pump_number,
															enum rapi_wdk_pump_position position,
															uint16_t test_time_s);


enum rapi_wdk_test_vfr
{
	rwtvFAIL,						// Some error occurred
	rwtvDEVICE_NOT_CONNECED,		// Device that owns output is disconnected
	rwtvDEVICE_IS_NOT_SYNCHRONIZED,	// Device that owns output has not synchronizad data (is in bootloader, just synchronizing, etc.)
	rwtvOID_IS_NOT_TESTABLE_OUTPUT,	// Device gien by device_serial_number has not VFR output
	rwtvSUCCESS,					// Output state is successfully set
};

enum rapi_wdk_vfr_position
{
	rwvpON,		// ON
	rwvpOFF,	// OFF
};

enum rapi_wdk_vfr_output
{
	// CCU VFR
	rwvoCCU_VFR_1,
	rwvoCCU_VFR_2,

	// EU-206-VFR
	rwvoEU_206_VFR_A,
	rwvoEU_206_VFR_B,
	rwvoEU_206_VFR_C,
	rwvoEU_206_VFR_D,
	rwvoEU_206_VFR_E,
	rwvoEU_206_VFR_F,
};

/**
 * roxi_api_wdk_test_vfr_callback
 *
 * It gives result about voltage free relays test
 *
 * Output:
 *  result: described in enum rapi_wdk_test_vfr
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_test_vfr_callback)(enum rapi_wdk_test_vfr result);

/**
 * roxi_api_wdk_test_voltage_free_relays
 *
 * It sets voltage free relay position to given value for given time duration
 * Output function should not be "off".
 *
 * Input:
 *  callback: described in roxi_api_wdk_test_vfr_callback
 *  device_serial_number: serial number of device with voltage free relay (CCU or EU-206_VFR)
 *  output_id: VFR id to remote. see enum rapi_wdk_vfr_output
 *  position: requested VFR position. see enum rapi_wdk_vfr_position
 *  test_time_s: after this time in seconds VFR returns into previous state
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_test_voltage_free_relays(roxi_api_wdk_test_vfr_callback callback,
																char *device_serial_number,
																enum rapi_wdk_vfr_output output_id,
																enum rapi_wdk_vfr_position position,
																uint16_t test_time_s);

enum rapi_wdk_get_thermoactuator_info
{
	rwgtiSUCCESS,	// Thermoactuator info successfully got
	rwgtiFAIL,		// Some error occured
};

enum roxi_api_wdk_thermoactuator_role
{
	rawtrRADIATOR,	// Thermoactuator is in radiator role
	rawtrFLOOR,		// Thermoactuator is in floor role
};

struct roxi_api_wdk_thermoactuator_info
{
	char									serial_number[18];	// Serial number of device with thermoactuator
	uint8_t									output_number;		// Number of thermoactuator in device
	uint8_t									load_detected;		// 1 if load was detected, 0 otherwise
	enum roxi_api_wdk_thermoactuator_role	role;				// described in enum roxi_api_wdk_thermoactuator_role
};

/**
 * roxi_api_wdk_get_thermoactuator_info_callback
 *
 * It gives result of get thermoactuator info
 *
 * Output:
 *  result: described in enum rapi_wdk_get_thermoactuator_info
 *  thermoactuator_array: array of thermoactuators. Item is described in struct roxi_api_wdk_thermoactuator_info
 *  thermoactuator_cnt: count of thermoactuators
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_get_thermoactuator_info_callback)(enum rapi_wdk_get_thermoactuator_info result,
																		struct roxi_api_wdk_thermoactuator_info *thermoactuator_array,
																		uint32_t thermoactuator_cnt);

/**
 * roxi_api_wdk_get_thermoactuator_info
 *
 * It gets information about thermoactuators
 *
 * Input:
 *  callback: described in roxi_api_wdk_get_thermoactuator_info_callback
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_get_thermoactuator_info(roxi_api_wdk_get_thermoactuator_info_callback callback);


enum rapi_wdk_get_room_hc_info
{
	rwgrhiSUCCESS,	// room hc info successfuly read
	rwgrhiFAIL,		// some error occurred
};

struct roxi_api_wdk_get_room_hc_info
{
	enum rapi_wdk_room	room;						// number of room
	uint8_t				has_radiator_hc_supplier;	// 1: room has radiator hc supplier, 0: otherwise
	char				radiator_supplier_name[257];// Name of supplier
	uint8_t				has_floor_hc_supplier;		// 1: room has floor hc supplier, 0: otherwise
	char				floor_supplier_name[257];	// Name of supplier
};

/**
 * roxi_api_wdk_get_room_hc_info_callback
 *
 * It gives result of room hc info
 *
 * output:
 *  result: described in enum rapi_wdk_get_room_hc_info
 *  room_array: array of rooms with hc information. Described in struct roxi_api_wdk_get_room_hc_info
 *  room_cnt: count of rooms
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_get_room_hc_info_callback)(enum rapi_wdk_get_room_hc_info result,
																	struct roxi_api_wdk_get_room_hc_info *room_array,
																	uint32_t room_cnt);

/**
 * roxi_api_wdk_get_room_hc_info
 *
 * It gets information about HC supplier for each room
 *
 * Input:
 *  callback: described in roxi_api_wdk_get_room_hc_info_callback
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_get_room_hc_info(roxi_api_wdk_get_room_hc_info_callback callback);


enum rapi_hcc_itc
{
	rhiITC1,	// ITC 1
	rhiITC2,	// ITC 2
	rhiHCC1,	// HCC 1
	rhiHCC2,	// HCC 2
};

enum rapi_wdk_get_hcc_itc_supplier
{
	rwghisSUCCESS,	// HCC/ITC supplier has successfuly got
	rwghisFAIL,		// Some error occurred
};

struct roxi_api_wdk_get_hcc_itc_supplier
{
	enum rapi_hcc_itc	hcc_itc;				// HCC/ITC. Described in enum rapi_wdk_get_hcc_itc_supplier
	uint8_t				has_hc_supplier;		// 1: HCC/ITC has HC supplier, 0: otherwise
	char				hc_supplier_name[257];	// Name of hc supplier if exsts
};

/**
 * roxi_api_wdk_get_hcc_itc_supplier_callback
 *
 * It gives result of HCC/ITC supplier info
 *
 * Output:
 *  result: described in enum rapi_wdk_get_hcc_itc_supplier
 *  hcc_itc_array: array of ITC/HCC items. Item is described in enum rapi_wdk_get_hcc_itc_supplier
 *  hcc_itc_cnt: count of HCC/ITC
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_get_hcc_itc_supplier_callback)(enum rapi_wdk_get_hcc_itc_supplier result,
																	struct roxi_api_wdk_get_hcc_itc_supplier *hcc_itc_array,
																	uint32_t hcc_itc_cnt);

/**
 * roxi_api_wdk_get_hcc_itc_supplier
 *
 * It loads supplier presence for each HCC/ITC
 *
 * Input:
 *  callback: described in roxi_api_wdk_get_hcc_itc_supplier_callback
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_get_hcc_itc_supplier(roxi_api_wdk_get_hcc_itc_supplier_callback callback);


enum rapi_itc
{
	riITC1,	// ITC 1
	riITC2,	// ITC 2
};

enum rapi_wdk_get_itc_outdoor_temp
{
	rwgiotSUCCESS,	// ITC outdoor tem successfully got
	rwgiotFAIL,		// some error occured
};

struct roxi_api_wdk_get_itc_outdoor_temp
{
	enum rapi_itc	itc;						// ITC number, see enum rapi_itc
	uint8_t			has_assigned_outdoor_temp;	// 1: ITC has assigned outdoor temperature
};

/**
 * roxi_api_wdk_get_itc_outdoor_temp_callback
 *
 * It gives result of loading presence outdoor temperature in ITC
 *
 * output:
 *  result: described in enum rapi_wdk_get_itc_outdoor_temp
 *  itc_array: array of ITC
 *  itc_cnt: ITC count
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_get_itc_outdoor_temp_callback)(enum rapi_wdk_get_itc_outdoor_temp result,
																	struct roxi_api_wdk_get_itc_outdoor_temp *itc_array,
																	uint32_t itc_cnt);

/**
 * roxi_api_wdk_get_itc_outdoor_temp
 *
 * It gets information about presence outdoor temp in ITC
 *
 * Input:
 *  callback: described in roxi_api_wdk_get_itc_outdoor_temp_callback
 *
 *  Return:
 *   0: wait for callback result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_get_itc_outdoor_temp(roxi_api_wdk_get_itc_outdoor_temp_callback callback);

/*
 * UPDATE SYSTEM
 */

/**
 * In this enumeration is described states and available remote functions
 * OK: represents call of roxi_api_wdk_update_via_autoupdate_ok function
 * CANCEL: represents call of roxi_api_wdk_update_via_autoupdate_cancel function
 */
enum roxi_api_wdk_update_via_autoupdate_state
{
	// Progress states
	rawuvasIDLE,					// OK -> CHECKING
	rawuvasCHECKING,
	rawuvasCHECKING_FAIL,			// OK -> IDLE
	rawuvasUPDATE_NOT_AVAILABLE,	// OK -> IDLE
	rawuvasUPDATE_AVAILABLE,		// OK -> UPDATING_CCU/UPDATING_PERIPHERAL, CANCEL -> IDLE
	rawuvasUPDATING_CCU,
	rawuvasUPDATING_PERIPHERAL,
	rawuvasUPDATE_REJECTED,			// OK -> IDLE
	rawuvasUPDATE_FAILED,			// OK -> IDLE
	rawuvasUPDATE_FINISHED,			// OK -> IDLE

	// End states
	rawuvaFAILED,					// Some error occurred
	rawuvaAUTOUPDATE_IS_DISABLED,	// Can not remote autoupdate because is disabled
	rawuvaEND,						// Remote of autoupdate finished properly
};

/**
 * roxi_api_wdk_update_via_autoupdate_callback
 *
 * It gives result or current progress of autoupdate
 *
 * Output:
 *  state: described in enum roxi_api_wdk_update_via_autoupdate_state
 *  online_devices: number of online devices, available in IDLE STATE
 *  offline_devices: number of offline devices, available in IDLE STATE
 *  stored_fw_package_name: name of stored FW package in CCU, available in IDLE state
 *  devices_to_update: number of devices to update, available in UPDATE_AVAILABLE state
 *  update_all_time: update time of all devices (seconds), available in UPDATE_AVAILABLE state
 *  update_ccu_time: update time of CCU only (seconds), available in UPDATE_AVAILABLE state
 *  progress_device_idx: Index of current updated peripheral, available in rawuvasUPDATING_PERIPHERAL state
 *  progress_device_percent: update progress percentage, available in rawuvasUPDATING_CCU (is estimated only) and rawuvasUPDATING_PERIPHERAL
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_update_via_autoupdate_callback)(enum roxi_api_wdk_update_via_autoupdate_state	state,
																										uint8_t		online_devices,
																										uint8_t		offline_devices,
																										char		stored_fw_package_name[257],
																										uint8_t		devices_to_update,
																										uint16_t	update_all_time,
																										uint16_t	update_ccu_time,
																										uint8_t		progress_device_idx,
																										uint8_t		progress_device_percent);

/**
 * roxi_api_wdk_update_via_autoupdate
 *
 * It starts remote autoupdate mechanism in CCU
 *
 * Input:
 *  callback: described in roxi_api_wdk_update_via_autoupdate_callback
 *
 *  Return:
 *   0: wait for callback state/result
 *   -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_update_via_autoupdate(roxi_api_wdk_update_via_autoupdate_callback callback);

/**
 * roxi_api_wdk_update_via_autoupdate_end
 *
 * When autoupdate is in progress states this function end remoting of autoupdate. Callback should return rawuvaEND state
 */
API_FUNC_PREFIX
void roxi_api_wdk_update_via_autoupdate_end(void);

/**
 * roxi_api_wdk_update_via_autoupdate_ok
 *
 * It can be called in autoupdate progress states. It can remote autoupdate as described in enum roxi_api_wdk_update_via_autoupdate_state
 *
 * Return:
 *  0: success
 *  -1: can not be called in this state
 */
API_FUNC_PREFIX
int roxi_api_wdk_update_via_autoupdate_ok(void);

/**
 * roxi_api_wdk_update_via_autoupdate_cancel
 *
 * It can be called in autoupdate progress states. It can remote autoupdate as described in enum roxi_api_wdk_update_via_autoupdate_state
 *
 * Return:
 *  0: success
 *  -1: can not be called in this state
 */
API_FUNC_PREFIX
int roxi_api_wdk_update_via_autoupdate_cancel(void);


enum roxi_api_wdk_direct_update_get_device_list
{
	rawdugdlSUCCESS,	// Device list successfully got
	rawdugdlFAIL,		// Some error occured
};

enum rapi_wdk_firmware_status
{
	awfsUNKNOWN,			// Device is not synchronized. Can not check if is new fw for device
	awfsUPDATE_NECESSARY,	// New FW for device found
	awfsDOWNGRADE_NECESSARY,// Device has FW, that has major version higher than fw file. It should be downdraded to avoid uncompatibility with old system
	awfsUP_TO_DATE,			// Device is up to date.
	awfsNO_UPDATE_FILE,		// Not found any fw file for this device
};

enum rapi_wdk_device_location
{
	rwdlGLOBAL,			// Global peripheral
	rwdlROOM_1,
	rwdlROOM_2,
	rwdlROOM_3,
	rwdlROOM_4,
	rwdlROOM_5,
	rwdlROOM_6,
	rwdlROOM_7,
	rwdlROOM_8,
	rwdlROOM_9,
	rwdlROOM_10,
	rwdlROOM_11,
	rwdlROOM_12,
	rwdlROOM_13,
	rwdlROOM_14,
	rwdlROOM_15,
	rwdlROOM_16,
	rwdlROOM_17,
	rwdlROOM_18,
	rwdlROOM_19,
	rwdlROOM_20,
	rwdlROOM_21,
	rwdlROOM_22,
	rwdlROOM_23,
	rwdlROOM_24,
	rwdlDHW		= 0xFE,	// Peripheral is inrolled into DHW
	rwdlCCU		= 0xFF,	// Device is CCU
};

struct roxi_api_wdk_direct_update_device_list
{
	uint32_t						index;					// Index of device
	char							serial_number[19];		// Serial number of device
	enum rapi_wdk_device_location	room;					// Room when device is enrolled, see enum rapi_wdk_device_location
	enum rapi_wdk_connection_status	connection_status;		// Connection status of device see enum rapi_wdk_connection_status
	char							current_version[128];	// String with current version installed in device
	char							available_version[128];	// String with version found in FW file
	enum rapi_wdk_firmware_status	firmware_status;		// Described in enum rapi_wdk_firmware_status
};

/**
 * roxi_api_wdk_direct_update_get_device_list_callback
 *
 * It gives result and device list with information about update availability
 *
 * Output:
 *  result: desctibed in enum roxi_api_wdk_direct_update_get_device_list
 *  device_list: list of devices with information about update availability. Item is described in struct roxi_api_wdk_direct_update_device_list
 *  device_cnt: count of devices
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_direct_update_get_device_list_callback)(enum roxi_api_wdk_direct_update_get_device_list	result,
																			struct roxi_api_wdk_direct_update_device_list		*device_list,
																			uint32_t											device_cnt);

/**
 * roxi_api_wdk_direct_update_get_device_list
 * When CCU is in bootloader, this function not works.
 * If in CCU is stored fw package from auto udate server wait 15 minutes and ccu should boot into application
 *
 * It loads list of devices with information about new firmware availability
 *
 * Input:
 *  callback: described in roxi_api_wdk_direct_update_get_device_list_callback
 *
 * Optional input:
 *  fw_dir: path to directory with fw files. When is not used, device list is just list of devices with their current firmware versions
 *
 * Return:
 *  0: wait for callback result
 *  -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_direct_update_get_device_list(roxi_api_wdk_direct_update_get_device_list_callback	callback,
																	char*													fw_dir);

enum roxi_api_wdk_direct_update
{
	// Result states
	rawduFAIL,							// Some error occured
	rawduUPDATE_SUCCESSFULLY_FINISHED,	// Update is successfully finished
	rawduTIMED_OUT,						// Reconnection to ccu after reboot timed out
	rawduRC_ERROR,						// Device rejected update and returns result code. This error can not be fixed by user

	// Progress states
	rawduCONNECTING_TO_DEVICE,			// Try to connect to device
	rawduSWITCHING_TO_BOOTLOADER,		// Device is switching to bootloader
	rawduUPDATING_DEVICE,				// Device is updating
	rawduSWITCHING_TO_APPLICATION,		// Device is switching to aplication after update
};

/**
 * roxi_api_wdk_direct_update_update_device_callback
 *
 * It gives result/progress of device update
 *
 * Output:
 *  result: described in enum roxi_api_wdk_direct_update
 *  data_sent: current bytes sent to device. Available in rawduUPDATING_DEVICE state
 *  fw_size: size of whole firmware in bytes. Available in rawduUPDATING_DEVICE state
 *  rc_error: number code of error returned from device. Available in rawduRC_ERROR state
 *  reboot_time: time in seconds that takes device to switch to bootloader/application.
 *               Available in rawduSWITCHING_TO_BOOTLOADER and rawduSWITCHING_TO_APPLICATION states
 */
typedef void (TYPEDEF_FUNC_PREFIX *roxi_api_wdk_direct_update_update_device_callback)(enum roxi_api_wdk_direct_update result,
																			uint32_t data_sent,
																			uint32_t fw_size,
																			uint32_t rc_error,
																			uint32_t reboot_time);

/**
 * roxi_api_wdk_direct_update_update_device
 *
 * It updates device by selecting device list index
 * It can be called when roxi_api_wdk_direct_update_get_device_list is called before
 * When CCU is in bootloader, this function not works.
 * If in CCU is stored fw package from auto udate server wait 15 minutes and ccu should boot into application
 *
 * Input:
 *  device_index: index of device from struct roxi_api_wdk_direct_update_device_list
 *
 * Return:
 *  0: wait for callback result
 *  -1: fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_direct_update_update_device(roxi_api_wdk_direct_update_update_device_callback callback, uint32_t device_index);

/**
 * @brief It gets current CCU unix timestamp
 *
 * @param unix_timestamp CCU unix timestamp is stored into.
 * @return 0 on success. -1 on fail
 */
API_FUNC_PREFIX
int roxi_api_wdk_get_ccu_unix_timestamp(uint32_t* unix_timestamp);

#endif /* SOURCEDLL_ROXI_API_WDK_H_ */
