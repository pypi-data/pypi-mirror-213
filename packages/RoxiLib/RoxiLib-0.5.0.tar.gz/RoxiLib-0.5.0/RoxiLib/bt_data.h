/*
 *  Created on: 28. 8. 2017
 *    Author: sindelar@jablotron.cz
 */

#ifndef BT_DATA_H_
#define BT_DATA_H_

#include <stdint.h>

#if (defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)) && defined(__GNUC__)
	  #define PACK_BT_DATA __attribute__((packed, gcc_struct))
#else
	  #define PACK_BT_DATA __attribute__((packed))
#endif

#ifndef STATIC_ASSERT
#define STATIC_ASSERT(expression, msg) typedef char static_assertion[(expression) ? 1 : -1]
#endif

/*
 * Abbreviations
 *
 * CTRL         Control
 * DHW          Domestic Hot Water
 * ECO          Economic
 * ENA          Enable
 * HCC          Heating/Cooling Control
 * HCW          Heating/Cooling Water
 * HUM          Humidity
 * ITC          Inlet Temperature Controller
 * LEL          Lower Explosive Limit
 * PERIPH       Peripheral
 * PWR          Power
 * TEMP         Temperature
 * VOC          Volatile Organic Compound
 */

#define BT_OBJ_NAME_LEN                     32

#define BT_VAL_D1_INVALID           (0x7F)
#define BT_VAL_D2_INVALID           (0x7FFF)
#define BT_VAL_D4_INVALID           (0x7FFFFFFF)
#define BT_VAL_U1_INVALID           (0xFF)
#define BT_VAL_U2_INVALID           (0xFFFF)
#define BT_VAL_U4_INVALID           (0xFFFFFFFF)
#define BT_VAL_REF_INVALID          (0xFFFFFFFF00000000)
#define BT_VAL_ENUM_INVALID         BT_VAL_U1_INVALID
#define BT_VAL_TEMP_INVALID         BT_VAL_D2_INVALID
#define BT_VAL_PERCENT_INVALID      BT_VAL_D2_INVALID

typedef enum bt_vtype
{
    // Special values
    BT_VTYPE_ARG_TIMESTAMP,
    BT_VTYPE_ARG_OID,
    BT_VTYPE_ARG_VID,
    BT_VTYPE_ARG_OVT,           // ALL ARGS TIMESTAMP, OID, VID (for start stream)

    // Basic data_types
    BT_VTYPE_D1 = 9,
    BT_VTYPE_D2,
    BT_VTYPE_D4,
    BT_VTYPE_U1,
    BT_VTYPE_U2,
    BT_VTYPE_U4,
    BT_VTYPE_TEXT,
    BT_VTYPE_DATA,
    BT_VTYPE_D2_FP10,
    BT_VTYPE_D2_FP100,
    BT_VTYPE_U2_FP10,
    BT_VTYPE_U2_FP100,

    // Derived data types
    BT_VTYPE_TIMESTAMP          = BT_VTYPE_U4,
    BT_VTYPE_OID_REF            = BT_VTYPE_U4,
    BT_VTYPE_VID_REF            = BT_VTYPE_U2,
    BT_VTYPE_TEMP               = BT_VTYPE_D2_FP100,
#define DegC                    (100)                   // example use set_temp(25.4 * DegC);
#define FP10                    (10)
    BT_VTYPE_PERCENT            = BT_VTYPE_D2_FP100,
#define Percent                 (100)
    BT_VTYPE_HUM                = BT_VTYPE_PERCENT,
    BT_VTYPE_VOLT               = BT_VTYPE_D2_FP100,
#define Volt                    (100)
    BT_VTYPE_ENUM               = BT_VTYPE_U1,
    BT_VTYPE_WARNING            = BT_VTYPE_U1,
    BT_VTYPE_BOOL               = BT_VTYPE_U1,
    BT_VTYPE_JOINT_WARNING      = BT_VTYPE_U4,
    BT_VTYPE_OBJ_INFO           = BT_VTYPE_U4,
} bt_val_type_t;


typedef enum
{
    BT_OBJ_TYPE_NETWORK,
    BT_OBJ_TYPE_LOCATION,
    BT_OBJ_TYPE_DEVICE,
    BT_OBJ_TYPE_INTERFACE,
    BT_OBJ_TYPE_INPUT,
    BT_OBJ_TYPE_OUTPUT,
    BT_OBJ_TYPE_ROOM,
    BT_OBJ_TYPE_ITC,
    BT_OBJ_TYPE_DHW,
    BT_OBJ_TYPE_HCC,
    BT_OBJ_TYPE_INPUT_OUTPUT,
    BT_OBJ_TYPE_DHW_TANK,
    BT_OBJ_TYPE_UPDATE,
    BT_OBJ_TYPE_PROFILE,
    BT_OBJ_TYPE_EDEV_MVDI,
    BT_OBJ_TYPE_DRYING,
    BT_OBJ_TYPE_INTEGRATION,
    BT_OBJ_TYPE_AGGREGATED_VALUES,
    BT_OBJ_TYPE_HCW_SOURCE,
    BT_OBJ_TYPE_HCW_SOURCE_ELEMENT,
    BT_OBJ_TYPE_GUI,
    BT_OBJ_TYPE_DHW_HEAT,
} bt_obj_type_t;

typedef enum
{
    BT_DEV_TYPE_DHW201			= 0x00,
    BT_DEV_TYPE_ITC202			= 0x01,
    BT_DEV_TYPE_TH201B			= 0x02,
    BT_DEV_TYPE_TH201R			= 0x03,
    BT_DEV_TYPE_LCD				= 0x04,
    BT_DEV_TYPE_RT210			= 0x05,
    BT_DEV_TYPE_RT250			= 0x06,
    BT_DEV_TYPE_RS211			= 0x07,
    BT_DEV_TYPE_RS251			= 0x08,
    BT_DEV_TYPE_RT250IR			= 0x09,
    BT_DEV_TYPE_EU208A			= 0x0A,
    BT_DEV_TYPE_EU206VFR		= 0x0B,
    BT_DEV_TYPE_ET250			= 0x0C,
    BT_DEV_TYPE_ET210			= 0x0D,
    BT_DEV_TYPE_VH250			= 0x0E,
    BT_DEV_TYPE_VH210			= 0x0F,
    BT_DEV_TYPE_DHW211_S        = 0xC0,
    BT_DEV_TYPE_DHW211_S_b      = 0xC1,
    BT_DEV_TYPE_DHW211_S_c      = 0xC2,
    BT_DEV_TYPE_DHW211          = 0xC3,
    BT_DEV_TYPE_DHW211_b        = 0xC4,
    BT_DEV_TYPE_DHW211_c        = 0xC5,
    BT_DEV_TYPE_DHW211_V        = 0xC6,
    BT_DEV_TYPE_DHW211_V_b      = 0xC7,
    BT_DEV_TYPE_DHW211_V_c      = 0xC8,
    BT_DEV_TYPE_DHW212_ITC      = 0xC9,
    BT_DEV_TYPE_DHW212_ITC_b    = 0xCA,
    BT_DEV_TYPE_DHW212_ITC_c    = 0xCB,
    BT_DEV_TYPE_DHW212_ITC_V    = 0xCC,
    BT_DEV_TYPE_DHW212_ITC_V_b  = 0xCD,
    BT_DEV_TYPE_DHW212_ITC_V_c  = 0xCE,
    BT_DEV_TYPE_DHW212_HC       = 0xCF,
    BT_DEV_TYPE_DHW212_HC_b     = 0xD0,
    BT_DEV_TYPE_DHW212_HC_c     = 0xD1,
    BT_DEV_TYPE_DHW212_HC_V     = 0xD2,
    BT_DEV_TYPE_DHW212_HC_V_b   = 0xD3,
    BT_DEV_TYPE_DHW212_HC_V_c   = 0xD4,
    BT_DEV_TYPE_CCU208          = 0xE0,
    BT_DEV_TYPE_PC_APP          = 0xFF
} bt_dev_type_t;

typedef enum
{
    BT_OUTPUT_SUBTYPE_PROFILE_THERMOHEAD,
    BT_OUTPUT_SUBTYPE_PROFILE_PUMP_RELAY,
    BT_OUTPUT_SUBTYPE_PROFILE_ANALOG,
    BT_OUTPUT_SUBTYPE_PROFILE_PWM,
    BT_OUTPUT_SUBTYPE_PROFILE_VFR,
    BT_OUTPUT_SUBTYPE_PROFILE_SERVO,
    BT_OUTPUT_SUBTYPE_THERMOHEAD,
    BT_OUTPUT_SUBTYPE_PUMP_RELAY,
    BT_OUTPUT_SUBTYPE_ANALOG,
    BT_OUTPUT_SUBTYPE_PWM,
    BT_OUTPUT_SUBTYPE_VFR,
    BT_OUTPUT_SUBTYPE_SERVO,
    BT_OUTPUT_SUBTYPE_PROFILE_VALVEHEAD,
    BT_OUTPUT_SUBTYPE_VALVEHEAD,
} bt_output_subtype_t;

typedef enum
{
    BT_ROOM_SUBTYPE_DEFAULT,
    BT_ROOM_SUBTYPE_NO_TEMP_SOURCES,
} bt_room_subtype_t;

typedef enum
{
    BT_EDEV_MVDI_SUBTYPE_GENERIC            = 0,
    BT_EDEV_MVDI_SUBTYPE_P300_S300,
    BT_EDEV_MVDI_SUBTYPE_PC300_SC300,
    BT_EDEV_MVDI_SUBTYPE_SCRKAE,
    BT_EDEV_MVDI_SUBTYPE_CMV_CLIMATIX_S300,
    BT_EDEV_MVDI_SUBTYPE_CMV_TITON,
    BT_EDEV_MVDI_SUBTYPE_CMV_GENERIC,
} bt_edev_mvdi_subtype_t;


#define BT_OBJ_INFO_GET_TYPE(obj_info)      ((obj_info) & 0xFF)
#define BT_OBJ_INFO_GET_SUBTYPE(obj_info)   (((obj_info) >> 8) & 0xFF)
#define BT_OBJ_INFO(type, subtype)          (((type) & 0xFF) | (((subtype) & 0xFF) << 8))


typedef uint32_t bt_vtpair_t;   // OPTIMIZE: make a global VTYPE table based on VID.

#define BT_VTPAIR(vid, vtype)   (((vid) & 0xFFFF) | ((vtype) << 16))
#define BT_VID(vtpair)          ((vtpair) & 0xFFFF)
#define BT_VTYPE(vtpair)        ((bt_val_type_t)(((vtpair) >> 16) & 0xFF))

//-------------------------------------------------------------------------------------------------------------------------

enum bt_enum_blocking {
    BT_ENUM_BLOCKING_NONE                       = 0,
    BT_ENUM_BLOCKING_UNKNOWN                    = 1,
    BT_ENUM_BLOCKING_CONTACT                    = 2,
    BT_ENUM_BLOCKING_FLOOR_TEMP                 = 3,
    BT_ENUM_BLOCKING_LOW_ENERGY                 = 4,
    BT_ENUM_BLOCKING_AIR_TEMP                   = 5,
    BT_ENUM_BLOCKING_DEW_POINT                  = 6,
    BT_ENUM_BLOCKING_OUTDOOR_TEMP               = 7,
    BT_ENUM_BLOCKING_FAULT                      = 8,
    BT_ENUM_BLOCKING_FAULT_HTCO                 = 9,
    BT_ENUM_BLOCKING_PERIODIC_ACTIVATION        = 10,
    BT_ENUM_BLOCKING_BMS_SYSTEM                 = 11,
    BT_ENUM_BLOCKING_DEADBAND                   = 12,
    BT_ENUM_BLOCKING_DRYING                     = 13,
    BT_ENUM_BLOCKING_SEASON                     = 14,
    BT_ENUM_BLOCKING_INSUFFICIENT_DEMAND        = 15,
    BT_ENUM_BLOCKING_COOLDOWN_PERIOD            = 16,
    BT_ENUM_BLOCKING_HCW_SOURCE_NOT_RELEASED    = 17,
    BT_ENUM_BLOCKING_ROOM_MODE                  = 18,
    BT_ENUM_BLOCKING_SYSTEM_INITIALIZING        = 19,
    BT_ENUM_BLOCKING_SYSTEM_SHUTDOWN            = 20,
    BT_ENUM_BLOCKING_NO_OUTPUT                  = 21,
    BT_ENUM_BLOCKING_FIRST_OPEN_ACTIVATION      = 22,
	BT_ENUM_BLOCKING_ROOM_WITH_NO_TEMP_SOURCES  = 23,
};

//-------------------------------------------------------------------------------------------------------------------------

#define BT_OBJECT_NAME                                          BT_VTPAIR( 0x8090, BT_VTYPE_TEXT)
#define BT_OBJECT_INFO                                          BT_VTPAIR( 0x809D, BT_VTYPE_U4)
#define BT_OBJECT_STATUS                                        BT_VTPAIR( 0x8439, BT_VTYPE_ENUM)
#define BT_OBJECT_RUNTIME_VAL_LIST                              BT_VTPAIR( 0x809F, BT_VTYPE_DATA)
#define BT_OBJECT_SERVICE_VAL_LIST                              BT_VTPAIR( 0x80AB, BT_VTYPE_DATA)
#define BT_OBJECT_PERIPHERAL_LIST                               BT_VTPAIR( 0x80AE, BT_VTYPE_DATA)
#define BT_AIR_TEMP                                             BT_VTPAIR( 0x0C  , BT_VTYPE_TEMP)
#define BT_FLOOR_TEMP                                           BT_VTPAIR( 0x0D  , BT_VTYPE_TEMP)
#define BT_HUMIDITY                                             BT_VTPAIR( 0x02  , BT_VTYPE_PERCENT)
#define BT_OUTDOOR_TEMP                                         BT_VTPAIR( 0x36  , BT_VTYPE_TEMP)
#define BT_DEW_POINT                                            BT_VTPAIR( 0x4B  , BT_VTYPE_TEMP)
#define BT_DEBUG_CHANNEL                                        BT_VTPAIR( 0x5F  , BT_VTYPE_TEXT)    // debug channel to LOOGER

enum bt_object_status {
    BT_OBJECT_STATUS_NORMAL             = 0,
    BT_OBJECT_STATUS_NEWLY_ADDED        = 1,
};

//-------------------------------------------------------------------------------------------------------------------------

#define BT_DHW_TEMP                                             BT_VTPAIR( 0x11  , BT_VTYPE_TEMP)
#define BT_DCW_TEMP                                             BT_VTPAIR( 0x14  , BT_VTYPE_TEMP)
#define BT_DCW_FLOW                                             BT_VTPAIR( 0x13  , BT_VTYPE_D2)

//-------------------------------------------------------------------------------------------------------------------------

#define BT_HCW_CONSUMERS_LIST                                   BT_VTPAIR( 0x80B8, BT_VTYPE_DATA)
#define BT_HCW_SUPPLYING_CONSUMERS_LIST                         BT_VTPAIR( 0x8144, BT_VTYPE_DATA)
#define BT_HCW_SUPPLIER_OID                                     BT_VTPAIR( 0x810C, BT_VTYPE_U4)
#define BT_HCW_REQUIRED_TEMP                                    BT_VTPAIR( 0x3A  , BT_VTYPE_TEMP)
#define BT_HCW_ACTUAL_OUTBOUND_TEMP                             BT_VTPAIR( 0x3E  , BT_VTYPE_TEMP)
#define BT_HCW_BLOCKING                                         BT_VTPAIR( 0x58  , BT_VTYPE_U1)
#define BT_HCW_SRC_DEMAND                                       BT_VTPAIR( 0x68  , BT_VTYPE_U1)
#define BT_HCW_SRC_DEMAND_STRUCT                                BT_VTPAIR( 0xA8  , BT_VTYPE_DATA)
#define BT_HCW_SRC_STATUS                                       BT_VTPAIR( 0xA9  , BT_VTYPE_DATA)
#define BT_HCW_INLET_TEMP                                       BT_VTPAIR( 0x19  , BT_VTYPE_TEMP)
#define BT_HCW_RETURN_TEMP                                      BT_VTPAIR( 0x1A  , BT_VTYPE_TEMP)
#define BT_HCW_SOURCE_INLET_TEMP                                BT_VTPAIR( 0x15  , BT_VTYPE_TEMP)
#define BT_HCW_SOURCE_RETURN_TEMP                               BT_VTPAIR( 0x16  , BT_VTYPE_TEMP)
#define BT_HCW_PRESSURE                                         BT_VTPAIR( 0x17  , BT_VTYPE_D2_FP100)

#define BT_HCW_AIR_SUPPLIER_OID                                 BT_VTPAIR( 0x8481, BT_VTYPE_U4)
#define BT_HCW_AIR_SRC_DEMAND                                   BT_VTPAIR( 0xB1  , BT_VTYPE_DATA)

#define BT_HCW_UFHC_SUPPLIER_OID                                BT_VTPAIR( 0x8482, BT_VTYPE_U4)
#define BT_HCW_UFHC_SRC_DEMAND                                  BT_VTPAIR( 0xB2  , BT_VTYPE_DATA)


typedef enum
{
    BT_HCW_STATE_OFF,
    BT_HCW_STATE_IDLE,
    BT_HCW_STATE_ACTIVATING,
    BT_HCW_STATE_ACTIVE,
} bt_hcw_state_t;


typedef struct {
    uint8_t primary     : 4;
    uint8_t secondary   : 4;
    uint8_t future      : 4;
    uint16_t requested_temp;
} bt_hcw_demand;


#define BT_HCW_DEMAND_PRIMARY_MASK                           (0x0F << 0)
#define BT_HCW_DEMAND_SECONDARY_MASK                         (0x0F << 4)
#define BT_HCW_DEMAND_FUTURE_MASK                            (0x0F << 8)


typedef struct {
    uint32_t activity               : 2;
    uint32_t freezing               : 1;
    uint32_t failure                : 1;
    uint32_t excess_energy          : 1;
    uint32_t insufficient_energy    : 1;
} bt_hcw_status;


typedef enum
{
    BT_HCW_STATUS_IDLE,
    BT_HCW_STATUS_PREPARE,
    BT_HCW_STATUS_ACTIVE,
    BT_HCW_STATUS_TERMINATE,
} bt_hcw_status_t;


#define BT_HCW_STATUS_ACTIVITY_MASK                          (0x03 << 0)
#define BT_HCW_STATUS_EXCESS_ENERGY_MASK                     (0x01 << 2)
#define BT_HCW_STATUS_INSUFFICIENT_ENERGY_MASK               (0x01 << 3)


//-------------------------------------------------------------------------------------------------------------------------

#define BT_AC_CONSUMER_LIST                                     BT_VTPAIR( 0x810D, BT_VTYPE_DATA)
#define BT_AC_SUPPLIER_OID                                      BT_VTPAIR( 0x810E, BT_VTYPE_U4)
#define BT_AC_REQUIRED_LEVEL                                    BT_VTPAIR( 0x57  , BT_VTYPE_U1)
#define BT_AC_BLOCKING                                          BT_VTPAIR( 0x59  , BT_VTYPE_U1)


//-------------------------------------------------------------------------------------------------------------------------

/**  \deprecated Renamed to BT_HUM_CTRL_PROGRAMMABLE_OUTPUT_LEVEL */
#define BT_DRY_SRC_DEMAND                                       BT_VTPAIR( 0x76  , BT_VTYPE_U1)

#define BT_DRYING_CONSUMER_LIST                                 BT_VTPAIR( 0x8429, BT_VTYPE_DATA)
#define BT_DRYING_SUPPLIER_OID                                  BT_VTPAIR( 0x842A, BT_VTYPE_OID_REF)
#define BT_DRYING_SRC_DEMAND                                    BT_VTPAIR( 0x98  , BT_VTYPE_DATA)
#define BT_DRYING_SRC_STATUS                                    BT_VTPAIR( 0x93  , BT_VTYPE_DATA)
#define BT_DRYING_BLOCKING                                      BT_VTPAIR( 0x94  , BT_VTYPE_ENUM)
#define BT_DRYING_STATE                                         BT_VTPAIR( 0x99  , BT_VTYPE_ENUM)


typedef enum
{
    BT_DRYING_STATE_OFF,
    BT_DRYING_STATE_IDLE,
    BT_DRYING_STATE_ACTIVATING,
    BT_DRYING_STATE_ACTIVE,
} bt_drying_state_t;


typedef struct {
    uint8_t primary     : 4;
    uint8_t secondary   : 4;
    uint8_t future      : 4;
    uint16_t reserved;
} bt_drying_demand;

/*typedef struct {
    uint32_t value;
} bt_drying_demand;*/

#define BT_DRYING_DEMAND_PRIMARY_MASK                           (0x0F << 0)
#define BT_DRYING_DEMAND_SECONDARY_MASK                         (0x0F << 4)
#define BT_DRYING_DEMAND_FUTURE_MASK                            (0x0F << 8)



typedef struct {
    uint32_t activity               : 2;
    uint32_t excess_energy          : 1;
    uint32_t insufficient_energy    : 1;
    uint32_t night_setback          : 1;
} bt_drying_status;

/*typedef struct {
    uint32_t value;
} bt_drying_status;*/


typedef enum
{
    BT_DRYING_STATUS_IDLE,
    BT_DRYING_STATUS_PREPARE,
    BT_DRYING_STATUS_ACTIVE,
    BT_DRYING_STATUS_TERMINATE,
} bt_drying_status_t;


#define BT_DRYING_STATUS_ACTIVITY_MASK                          (0x03 << 0)
#define BT_DRYING_STATUS_EXCESS_ENERGY_MASK                     (0x01 << 2)
#define BT_DRYING_STATUS_INSUFFICIENT_ENERGY_MASK               (0x01 << 3)

//-------------------------------------------------------------------------------------------------------------------------

#define BT_INTEGRATION_CONSUMER_LIST                            BT_VTPAIR( 0x842E, BT_VTYPE_DATA)
#define BT_INTEGRATION_SUPPLIER_OID                             BT_VTPAIR( 0x842F, BT_VTYPE_OID_REF)
#define BT_INTEGRATION_SRC_DEMAND                               BT_VTPAIR( 0x95  , BT_VTYPE_DATA)
#define BT_INTEGRATION_SRC_STATUS                               BT_VTPAIR( 0x96  , BT_VTYPE_DATA)
#define BT_INTEGRATION_BLOCKING                                 BT_VTPAIR( 0x97  , BT_VTYPE_ENUM)
#define BT_INTEGRATION_STATE                                    BT_VTPAIR( 0x9A  , BT_VTYPE_ENUM)


typedef enum
{
    BT_INTEGRATION_STATE_OFF,
    BT_INTEGRATION_STATE_IDLE,
    BT_INTEGRATION_STATE_ACTIVATING_HEATING,
    BT_INTEGRATION_STATE_ACTIVE_HEATING,
    BT_INTEGRATION_STATE_ACTIVATING_COOLING,
    BT_INTEGRATION_STATE_ACTIVE_COOLING,
} bt_integration_state_t;


typedef struct {
    uint8_t primary     : 4;
    uint8_t secondary   : 4;
    uint8_t future      : 4;
    uint16_t requested_temp;
} bt_integration_demand;

/*typedef struct {
    uint32_t value;
} bt_integration_demand;*/

#define BT_INTEGRATION_DEMAND_PRIMARY_MASK                      (0x0F << 0)
#define BT_INTEGRATION_DEMAND_SECONDARY_MASK                    (0x0F << 4)
#define BT_INTEGRATION_DEMAND_FUTURE_MASK                       (0x0F << 8)


typedef struct {
    uint32_t activity               : 2;
    uint32_t excess_energy          : 1;
    uint32_t insufficient_energy    : 1;
} bt_integration_status;

/*typedef struct {
    uint32_t value;
} bt_integration_status;*/


typedef enum
{
    BT_INTEGRATION_STATUS_IDLE,
    BT_INTEGRATION_STATUS_PREPARE,
    BT_INTEGRATION_STATUS_ACTIVE,
    BT_INTEGRATION_STATUS_TERMINATE,
} bt_integration_status_t;


#define BT_INTEGRATION_STATUS_ACTIVITY_MASK                     (0x03 << 0)
#define BT_INTEGRATION_STATUS_EXCESS_ENERGY_MASK                (0x01 << 2)
#define BT_INTEGRATION_STATUS_INSUFFICIENT_ENERGY_MASK          (0x01 << 3)


//-------------------------------------------------------------------------------------------------------------------------

#define BT_VENTILATION_CONSUMER_LIST                            BT_VTPAIR( 0x84C6, BT_VTYPE_DATA)
#define BT_VENTILATION_SUPPLIER_OID                             BT_VTPAIR( 0x84C7, BT_VTYPE_OID_REF)
#define BT_VENTILATION_SRC_DEMAND                               BT_VTPAIR( 0xF0  , BT_VTYPE_DATA)
#define BT_VENTILATION_SRC_STATUS                               BT_VTPAIR( 0xF1  , BT_VTYPE_DATA)
#define BT_VENTILATION_STATE                                    BT_VTPAIR( 0xF5  , BT_VTYPE_DATA)


typedef enum
{
    BT_VENTILATION_STATE_OFF,
    BT_VENTILATION_STATE_STOPPED,
    BT_VENTILATION_STATE_UNOCCUPIED,
    BT_VENTILATION_STATE_ECO,
    BT_VENTILATION_STATE_COMFORT,
    BT_VENTILATION_STATE_BOOST,
    BT_VENTILATION_STATE_BLOCKED,
    BT_VENTILATION_STATE_FAILURE,
} bt_ventilation_state_state_t;


typedef struct {
	uint32_t state              : 8;  // See #bt_ventilation_state_state_t
	uint32_t blocking           : 8;  // See #bt_enum_blocking
	uint32_t                    :16;  // Reserved, zero
} bt_ventilation_state_t;


// TODO
typedef struct {
    uint8_t primary     : 4;
} bt_ventilation_demand;



typedef enum
{
    BT_VENTILATION_STATUS_STATUS_OFF,
    BT_VENTILATION_STATUS_STATUS_NORMAL_OPERATION,
    BT_VENTILATION_STATUS_STATUS_MAINTENANCE,
    BT_VENTILATION_STATUS_STATUS_UNKNOWN,
    BT_VENTILATION_STATUS_STATUS_FAILURE, // Device disconnected or critical alarm
} bt_ventilation_status_status_t;


typedef enum
{
    BT_VENTILATION_LEVEL_STOPPED,
    BT_VENTILATION_LEVEL_UNOCCUPIED,
    BT_VENTILATION_LEVEL_ECO,
    BT_VENTILATION_LEVEL_COMFORT,
    BT_VENTILATION_LEVEL_BOOST,
} bt_ventilation_level_t;


typedef struct {
    uint32_t status             : 4;  // See #bt_ventilation_status_status_t
    uint32_t required_level     : 4;  // See #bt_ventilation_level_t
    uint32_t actual_level       : 4;  // See #bt_ventilation_level_t
    uint32_t blocking           : 8;  // See #bt_enum_blocking
    uint32_t                    :12;  // Reserved, zeroed
} bt_ventilation_status_t;


//-------------------------------------------------------------------------------------------------------------------------

#define BT_HCWS_STATUS                                          BT_VTPAIR( 0xA4  , BT_VTYPE_ENUM)
#define BT_HCWS_SOURCE_ELEMENT_LIST                             BT_VTPAIR( 0x844B, BT_VTYPE_DATA)
//#define BT_HCWS_INLET_TEMP_SOURCE                             BT_VTPAIR(       , BT_VTYPE_DATA)
#define BT_HCWS_ERR_INLET_SENSOR_FAIL                           BT_VTPAIR( 0x4047, BT_VTYPE_WARNING)
#define BT_HCWS_DEMAND_START_DELAY                              BT_VTPAIR( 0x8452, BT_VTYPE_U2)
#define BT_HCWS_DEMAND_STOP_DELAY                               BT_VTPAIR( 0x8453, BT_VTYPE_U2)
#define BT_HCWS_DEMAND_COOLDOWN_TIME                            BT_VTPAIR( 0x8451, BT_VTYPE_U2)
#define BT_HCWS_INLET_TEMP_SOURCE                               BT_VTPAIR( 0x8456, BT_VTYPE_DATA)
#define BT_HCWS_LAST_DEMAND                                     BT_VTPAIR( 0xAA  , BT_VTYPE_TIMESTAMP)

#define BT_HCWS_ERR_SOURCE_FAIL                                 BT_VTPAIR( 0x4048, BT_VTYPE_WARNING)
#define BT_HCWS_ERR_SOURCE_GENERAL_FAIL                         BT_VTPAIR( 0x4049, BT_VTYPE_WARNING)
#define BT_HCWS_SOURCE_RELEASE                                  BT_VTPAIR( 0xA7  , BT_VTYPE_ENUM)
#define BT_HCWS_ANALOG_DEMAND                                   BT_VTPAIR( 0xA5  , BT_VTYPE_D2_FP100)
#define BT_HCWS_BINARY_DEMAND                                   BT_VTPAIR( 0xA6  , BT_VTYPE_D2_FP100)
#define BT_HCWS_HEAT_ANALOG_CURVE_P1_VOLTAGE                    BT_VTPAIR( 0x8446, BT_VTYPE_D2_FP100)
#define BT_HCWS_HEAT_ANALOG_CURVE_P1_TEMP                       BT_VTPAIR( 0x8447, BT_VTYPE_TEMP)
#define BT_HCWS_HEAT_ANALOG_CURVE_P2_VOLTAGE                    BT_VTPAIR( 0x8448, BT_VTYPE_D2_FP100)
#define BT_HCWS_HEAT_ANALOG_CURVE_P2_TEMP                       BT_VTPAIR( 0x8449, BT_VTYPE_TEMP)
#define BT_HCWS_HEAT_ANALOG_CURVE_NO_DEMAND_THRESHOLD           BT_VTPAIR( 0x844A, BT_VTYPE_TEMP)
#define BT_HCWS_COOL_ANALOG_CURVE_P1_VOLTAGE                    BT_VTPAIR( 0x844C, BT_VTYPE_D2_FP100)
#define BT_HCWS_COOL_ANALOG_CURVE_P1_TEMP                       BT_VTPAIR( 0x844D, BT_VTYPE_TEMP)
#define BT_HCWS_COOL_ANALOG_CURVE_P2_VOLTAGE                    BT_VTPAIR( 0x844E, BT_VTYPE_D2_FP100)
#define BT_HCWS_COOL_ANALOG_CURVE_P2_TEMP                       BT_VTPAIR( 0x844F, BT_VTYPE_TEMP)
#define BT_HCWS_COOL_ANALOG_CURVE_NO_DEMAND_THRESHOLD           BT_VTPAIR( 0x8450, BT_VTYPE_TEMP)
#define BT_HCWS_RELEASE_OUTDOOR_TEMP                            BT_VTPAIR( 0x8454, BT_VTYPE_TEMP)
#define BT_HCWS_UNRELEASE_OUTDOOR_TEMP                          BT_VTPAIR( 0x8455, BT_VTYPE_TEMP)

typedef enum
{
    BT_HCWS_SOURCE_STATUS_IDLE,
    BT_HCWS_SOURCE_STATUS_PREPARE,
    BT_HCWS_SOURCE_STATUS_ACTIVE,
    BT_HCWS_SOURCE_STATUS_TERMINATE,
} bt_hcws_source_status_t;

//-------------------------------------------------------------------------------------------------------------------------

#define BT_CONTROLLER_ASSOCIATED_MAP_INDEX                      BT_VTPAIR( 0x8424, BT_VTYPE_U1)
#define BT_CONTROLLER_ASSOCIATED_MAP_INDEX_OFFSET               BT_VTPAIR( 0x8425, BT_VTYPE_U1)

//-------------------------------------------------------------------------------------------------------------------------

#define BT_LOCATION_LANGUAGE                                    BT_VTPAIR( 0x805E, BT_VTYPE_ENUM)
#define BT_LOCATION_TIMEZONE                                    BT_VTPAIR( 0x806F, BT_VTYPE_TEXT)
#define BT_LOCATION_TIMEZONE_OFFSET                             BT_VTPAIR( 0x8074, BT_VTYPE_D4)
#define BT_LOCATION_TIMEZONE_DST_ENABLED                        BT_VTPAIR( 0x8075, BT_VTYPE_U1)
#define BT_LOCATION_LOCAL_TIME_OFFSET                           BT_VTPAIR( 0x2E  , BT_VTYPE_D4)
#define BT_LOCATION_COUNTRY                                     BT_VTPAIR( 0x8486, BT_VTYPE_ENUM)
#define BT_LOCATION_VACATION                                    BT_VTPAIR( 0x8085, BT_VTYPE_U1)
#define BT_LOCATION_VACATION_END_TIME                           BT_VTPAIR( 0x8086, BT_VTYPE_TIMESTAMP)
#define BT_LOCATION_HC_MODE_SWITCHING                           BT_VTPAIR( 0x8076, BT_VTYPE_ENUM)
#define BT_LOCATION_HC_MODE                                     BT_VTPAIR( 0x803D, BT_VTYPE_ENUM)
#define BT_LOCATION_HC_MODE_PRIORITY                            BT_VTPAIR( 0x84DF, BT_VTYPE_ENUM)
#define BT_LOCATION_HC_MODE_BMS_OVERRIDE                        BT_VTPAIR( 0x84E0, BT_VTYPE_ENUM)
#define BT_LOCATION_HC_MODE_HW_SOURCE                           BT_VTPAIR( 0x84E3, BT_VTYPE_DATA)
#define BT_LOCATION_HC_MODE_HEATING_SINCE                       BT_VTPAIR( 0x8077, BT_VTYPE_TIMESTAMP)
#define BT_LOCATION_HC_MODE_COOLING_SINCE                       BT_VTPAIR( 0x8041, BT_VTYPE_TIMESTAMP)
#define BT_LOCATION_HC_HEATING_MAX_OUTDOOR_TEMP                 BT_VTPAIR( 0x8140, BT_VTYPE_TEMP)
#define BT_LOCATION_HC_COOLING_MIN_OUTDOOR_TEMP                 BT_VTPAIR( 0x80FF, BT_VTYPE_TEMP)
#define BT_LOCATION_HC_DEW_POINT_OFFSET                         BT_VTPAIR( 0x8100, BT_VTYPE_TEMP)
#define BT_LOCATION_HC_DEADBAND_TEMP                            BT_VTPAIR( 0x80FB, BT_VTYPE_TEMP)
#define BT_LOCATION_HC_MODE_SWITCH_COOLDOWN                     BT_VTPAIR( 0x80FC, BT_VTYPE_U4)
#define BT_LOCATION_HC_MODE_LAST_TRANSITION                     BT_VTPAIR( 0x80F5, BT_VTYPE_U4)
#define BT_LOCATION_HC_AUTO_SWITCHING_SAMPLES                   BT_VTPAIR( 0x84E4, BT_VTYPE_DATA)
#define BT_LOCATION_HC_AUTO_SWITCHING_HEATING_CONSECUTIVE_DAYS          BT_VTPAIR( 0x84E5, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_HEATING_INTERMITTENT_DAYS         BT_VTPAIR( 0x84E6, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_HEATING_INTERMITTENT_DAYS_PERIOD  BT_VTPAIR( 0x84E7, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_HEATING_PERIOD_LENGTH             BT_VTPAIR( 0x84E8, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_COOLING_CONSECUTIVE_DAYS          BT_VTPAIR( 0x84E9, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_COOLING_INTERMITTENT_DAYS         BT_VTPAIR( 0x84EA, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_COOLING_INTERMITTENT_DAYS_PERIOD  BT_VTPAIR( 0x84EB, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_COOLING_PERIOD_LENGTH             BT_VTPAIR( 0x84EC, BT_VTYPE_U1)
#define BT_LOCATION_HC_AUTO_SWITCHING_PERIOD_TIMER              BT_VTPAIR( 0x10F , BT_VTYPE_TIMESTAMP)
#define BT_LOCATION_STANDBY                                     BT_VTPAIR( 0x8087, BT_VTYPE_U1)
#define BT_LOCATION_WARNING_DEV_SERVICE                         BT_VTPAIR( 0x4013, BT_VTYPE_WARNING)
#define BT_LOCATION_WARNING_FAULT                               BT_VTPAIR( 0x4014, BT_VTYPE_WARNING)
#define BT_LOCATION_GLOBAL_PERIPH_LIST                          BT_OBJECT_PERIPHERAL_LIST
#define BT_LOCATION_LEARN_DEST_OID                              BT_VTPAIR( 0x80AC, BT_VTYPE_DATA)
#define BT_LOCATION_LEARN_PERIPH_DESC                           BT_VTPAIR( 0x80AD, BT_VTYPE_U4)
#define BT_LOCATION_CONTROL_UNIT_OID                            BT_VTPAIR( 0x80DC, BT_VTYPE_U4)
#define BT_LOCATION_RECYCLE_BIN                                 BT_VTPAIR( 0x80E6, BT_VTYPE_DATA)
#define BT_LOCATION_COMMAND                                     BT_VTPAIR( 0x42  , BT_VTYPE_U1)
#define BT_LOCATION_EMULATE_FAIL                                BT_VTPAIR( 0x12  , BT_VTYPE_ENUM)
#define BT_LOCATION_HARDWARE_PROFILE                            BT_VTPAIR( 0x80E8, BT_VTYPE_U1)
#define BT_LOCATION_NEW_HARDWARE_PROFILE                        BT_VTPAIR( 0x80EE, BT_VTYPE_U1)
#define BT_LOCATION_STRUCTURE_ID                                BT_VTPAIR( 0x80F2, BT_VTYPE_U4)
#define BT_LOCATION_OUTDOOR_TEMP_SOURCE                         BT_VTPAIR( 0x80EF, BT_VTYPE_U4)
#define BT_LOCATION_OUTDOOR_TEMP_SOURCE_OVI                     BT_VTPAIR( 0x8466, BT_VTYPE_DATA)
#define BT_LOCATION_OUTDOOR_FILTER_SUPPRESSION                  BT_VTPAIR( 0x80DA, BT_VTYPE_U1)
#define BT_LOCATION_OUTDOOR_TEMP_FILTER_SETTINGS                BT_VTPAIR( 0x84ED, BT_VTYPE_DATA)
#define BT_LOCATION_SNAPSHOT_BACKUP                             BT_VTPAIR( 0x51  , BT_VTYPE_U1)
#define BT_LOCATION_SNAPSHOT_RESTORE                            BT_VTPAIR( 0x52  , BT_VTYPE_U1)
#define BT_LOCATION_ALARM_HEAT_PUMP_FAULT                       BT_VTPAIR( 0x401D, BT_VTYPE_WARNING)
#define BT_LOCATION_FROSTING_AIR_TEMP_THRESHOLD                 BT_VTPAIR( 0x813D, BT_VTYPE_TEMP)
#define BT_LOCATION_FROSTING_INLET_TEMP_THRESHOLD               BT_VTPAIR( 0x813E, BT_VTYPE_TEMP)
#define BT_LOCATION_FROSTING_OUTDOOR_TEMP_THRESHOLD             BT_VTPAIR( 0x813F, BT_VTYPE_TEMP)
#define BT_LOCATION_FILTERED_OUTDOOR_TEMP                       BT_VTPAIR( 0x28  , BT_VTYPE_TEMP)
#define BT_LOCATION_AVERAGE_OUTDOOR_TEMP                        BT_VTPAIR( 0x5E  , BT_VTYPE_TEMP)
#define BT_LOCATION_EXPRESS_MODE_END_TIME                       BT_VTPAIR( 0x8125, BT_VTYPE_U4)
#define BT_LOCATION_SUPPORT_MODE                                BT_VTPAIR( 0x8060, BT_VTYPE_U1)
#define BT_LOCATION_MODBUS_MODE                                 BT_VTPAIR( 0x8035, BT_VTYPE_ENUM)
#define BT_LOCATION_MODBUS_ADDR                                 BT_VTPAIR( 0x8036, BT_VTYPE_U1)
#define BT_LOCATION_MODBUS_BAUDRATE                             BT_VTPAIR( 0x8037, BT_VTYPE_U4)
#define BT_LOCATION_MODBUS_PARITY                               BT_VTPAIR( 0x8420, BT_VTYPE_ENUM)
#define BT_LOCATION_MODBUS_STOP_BITS                            BT_VTPAIR( 0x8421, BT_VTYPE_ENUM)
#define BT_LOCATION_MODBUS_PASSWORD                             BT_VTPAIR( 0x814B, BT_VTYPE_U2)
#define BT_LOCATION_INSTALLER_PASSWORD                          BT_VTPAIR( 0x8126, BT_VTYPE_TEXT)
//#define BT_LOCATION_SERVICE_KEY                               BT_VTPAIR( 0x6F  , BT_VTYPE_TEXT) // Deprecated, wrong VTYPE
#define BT_LOCATION_SERVICE_KEY                                 BT_VTPAIR( 0x7E  , BT_VTYPE_DATA)
#define BT_LOCATION_ALLOW_SERVICE_ACCESS                        BT_VTPAIR( 0x8134, BT_VTYPE_U1)
#define BT_LOCATION_ALLOW_DEVELOPMENT_FEATURES                  BT_VTPAIR( 0x8143, BT_VTYPE_U1)
#define BT_LOCATION_ALLOW_TEST_MODE                             BT_VTPAIR( 0x8147, BT_VTYPE_U1)
#define BT_LOCATION_CLOUD_ADDRESS_OVERRIDE                      BT_VTPAIR( 0x814E, BT_VTYPE_U4)
#define BT_LOCATION_CLOUD_KEY_OVERRIDE                          BT_VTPAIR( 0x107,  BT_VTYPE_DATA)
#define BT_LOCATION_ERR_EXT_DEVICE_FAIL                         BT_VTPAIR( 0x4044, BT_VTYPE_WARNING)
#define BT_LOCATION_REPUBLISH_PERIOD_TIME                       BT_VTPAIR( 0x8445, BT_VTYPE_U4)
#define BT_LOCATION_SYSLOG_CHANGE_DEST_IP                       BT_VTPAIR( 0x8461, BT_VTYPE_U4)
#define BT_LOCATION_SYSLOG_CHANGE_DEST_PORT                     BT_VTPAIR( 0x847A, BT_VTYPE_U2)
#define BT_LOCATION_WARN_MAINTENANCE                            BT_VTPAIR( 0x4050, BT_VTYPE_ENUM)
#define BT_LOCATION_EXERCISING_SCHEDULE                         BT_VTPAIR( 0x8488, BT_VTYPE_DATA)
#define BT_LOCATION_EXERCISING_SCHEDULE_OVERRIDE                BT_VTPAIR( 0xBD  , BT_VTYPE_U4)
#define BT_LOCATION_EXERCISING_SCHEDULE_OVERRIDE_SETUP          BT_VTPAIR( 0xF2  , BT_VTYPE_DATA)
#define BT_LOCATION_EXERCISING_LAST_ACTIVATION                  BT_VTPAIR( 0x8489, BT_VTYPE_U4)
#define BT_LOCATION_DEBUG_LEVEL                                 BT_VTPAIR( 0x848A, BT_VTYPE_U4)
#define BT_LOCATION_BACKEND_PKT_SENT_STATISTICS                 BT_VTPAIR( 0xF6  , BT_VTYPE_U4)
#define BT_LOCATION_BACKEND_PKT_SENT_AVERAGE                    BT_VTPAIR( 0xF7  , BT_VTYPE_U4)
#define BT_LOCATION_GENERATE_TEMPORARY_PASSWORD                 BT_VTPAIR( 0xFA  , BT_VTYPE_U4)
#define BT_LOCATION_TEMPORARY_PASSWORD                          BT_VTPAIR( 0xFD  , BT_VTYPE_TEXT)
#define BT_LOCATION_TEMPORARY_PASSWORD_EXPIRATION               BT_VTPAIR( 0xFE  , BT_VTYPE_U4)
#define BT_LOCATION_DEFAULT_LANGUAGE                            BT_VTPAIR( 0xFF  , BT_VTYPE_ENUM)
#define BT_LOCATION_BEHAVIOUR_VARIANT                           BT_VTPAIR( 0x100 , BT_VTYPE_U1)

enum bt_location_country
{
    BT_LOCATION_COUNTRY_NA,
    BT_LOCATION_COUNTRY_CZECH_REPUBLIC,
    BT_LOCATION_COUNTRY_DENMARK,
    BT_LOCATION_COUNTRY_UNITED_KINGDOM,
    BT_LOCATION_COUNTRY_GERMANY,
    BT_LOCATION_COUNTRY_ITALY,
    BT_LOCATION_COUNTRY_NETHERLANDS,
    BT_LOCATION_COUNTRY_FRANCE,
    BT_LOCATION_COUNTRY_SLOVAKIA,
    BT_LOCATION_COUNTRY_POLAND,
    BT_LOCATION_COUNTRY_LITHUANIA,
    BT_LOCATION_COUNTRY_RUSSIA,
    BT_LOCATION_COUNTRY_LATVIA,
    BT_LOCATION_COUNTRY_TURKEY,
    BT_LOCATION_COUNTRY_SWEDEN,
    BT_LOCATION_COUNTRY_FINLAND,
    BT_LOCATION_COUNTRY_HUNGARY,
    BT_LOCATION_COUNTRY_NORWAY,
    BT_LOCATION_COUNTRY_SPAIN,
};

enum bt_location_command
{
    BT_LOCATION_COMMAND_NONE,
    BT_LOCATION_COMMAND_RESET,
    BT_LOCATION_COMMAND_NET_LEARN,
};

enum bt_location_emulate_fail
{
    BT_LOCATION_EMULATE_FAIL_NONE,
    BT_LOCATION_EMULATE_FAIL_REJECT_UPDATE,
    BT_LOCATION_EMULATE_FAIL_BLOCK_CLOUD_YTUN,
    BT_LOCATION_EMULATE_FAIL_BLOCK_FW_YTUN
};

enum bt_location_language {
    BT_LOCATION_LANGUAGE_DEFAULT            = 0,
    BT_LOCATION_LANGUAGE_DANISH             = 1,
    BT_LOCATION_LANGUAGE_CZECH              = 2,
    BT_LOCATION_LANGUAGE_DUTCH              = 3,
    BT_LOCATION_LANGUAGE_TURKISH            = 4,
    BT_LOCATION_LANGUAGE_POLISH             = 5,
    BT_LOCATION_LANGUAGE_SWEDISH            = 6,
    BT_LOCATION_LANGUAGE_FRENCH             = 7,
    BT_LOCATION_LANGUAGE_GERMAN             = 8,
    BT_LOCATION_LANGUAGE_HUNGARIAN          = 9,
    BT_LOCATION_LANGUAGE_ITALIAN            = 10,
    BT_LOCATION_LANGUAGE_LATVIAN            = 11,
    BT_LOCATION_LANGUAGE_LITHUANIAN         = 12,
    BT_LOCATION_LANGUAGE_NORWEGIAN          = 13,
    BT_LOCATION_LANGUAGE_FINNISH 	        = 14,
    BT_LOCATION_LANGUAGE_SPANISH 	        = 15,
    BT_LOCATION_LANGUAGE_RUSSIAN 	        = 16,

    BT_LOCATION_LANGUAGE_ENGLISH            = BT_LOCATION_LANGUAGE_DEFAULT,
};

enum bt_location_vacation {
    BT_LOCATION_VACATION_OFF                = 0,
    BT_LOCATION_VACATION_ON                 = 1,
};

enum bt_location_hc_mode_switching {
    BT_LOCATION_HC_MODE_SWITCHING_NONE      = 0,
    BT_LOCATION_HC_MODE_SWITCHING_MANUAL    = 1,
    BT_LOCATION_HC_MODE_SWITCHING_CALENDAR  = 2,
    BT_LOCATION_HC_MODE_SWITCHING_DEADBAND  = 3,
    BT_LOCATION_HC_MODE_SWITCHING_INPUT     = 4,
};

enum bt_location_hc_mode {
    BT_LOCATION_HC_MODE_HEATING             = 0,
    BT_LOCATION_HC_MODE_COOLING             = 1
};

enum bt_location_hc_mode_priority_source {
    BT_LOCATION_HC_MODE_PRIORITY_SW         = 0,
    BT_LOCATION_HC_MODE_PRIORITY_HW,
};

enum bt_location_hc_mode_bms_override {
    BT_LOCATION_HC_MODE_BMS_OVERRIDE_INACTIVE   = 0,
    BT_LOCATION_HC_MODE_BMS_OVERRIDE_ACTIVE,
};

enum bt_location_support_mode {
    BT_LOCATION_SUPPORT_MODE_DISABLED       = 0,
    BT_LOCATION_SUPPORT_MODE_ENABLED        = 1
};

enum bt_location_modbus_mode {
    BT_LOCATION_MODBUS_MODE_DISABLED             = 0,
    BT_LOCATION_MODBUS_MODE_READ_ONLY            = 1,
    BT_LOCATION_MODBUS_MODE_READ_WRITE           = 2,
    BT_LOCATION_MODBUS_MODE_WRITE_WITH_PASSWORD  = 3,
};

enum bt_location_allow_service_access {
    BT_LOCATION_ALLOW_SERVICE_ACCESS_DISABLED	= 0,
    BT_LOCATION_ALLOW_SERVICE_ACCESS_ENABLED	= 1,
};

enum bt_location_profile {
    BT_LOCATION_PROFILE_1_0                     = 0,
    BT_LOCATION_PROFILE_1_1                     = 1,
    BT_LOCATION_PROFILE_1_2                     = 2,
    BT_LOCATION_PROFILE_1_3_1                   = 3,
    BT_LOCATION_PROFILE_1_3_2                   = 4,
    BT_LOCATION_PROFILE_2_1                     = 5,
    BT_LOCATION_PROFILE_2_2_1                   = 6,
    BT_LOCATION_PROFILE_3_3_0                   = 7,
    BT_LOCATION_PROFILE_3_3_1                   = 8,
    BT_LOCATION_PROFILE_3_3_2                   = 9,
    BT_LOCATION_PROFILE_3_3_3                   = 10,
    BT_LOCATION_PROFILE_2_2_2                   = 11,
    BT_LOCATION_PROFILE_1_0_1                   = 12,
    BT_LOCATION_PROFILE_1_1_1                   = 13,
    BT_LOCATION_PROFILE_1_9                     = 14,
    BT_LOCATION_PROFILE_2_1_0                   = 15,
    BT_LOCATION_PROFILE_4_1_1                   = 16,
    BT_LOCATION_PROFILE_4_1_4                   = 17,
    BT_LOCATION_PROFILE_4_1_3                   = 18,
    BT_LOCATION_PROFILE_4_1_2                   = 19,
};

typedef enum bt_location_maintenance_mode
{
    BT_LOCATION_MAINTENANCE_MODE_NONE = 0,
    BT_LOCATION_MAINTENANCE_MODE_EXERCISING, // For backward compatibility with TM60010.4 and lower
    BT_LOCATION_MAINTENANCE_MODE_PERIODIC_ACTIVATION,
    BT_LOCATION_MAINTENANCE_MODE_FIRST_OPEN_ACTIVATION,
} bt_location_maintenance_mode;


typedef struct bt_location_exercising_schedule_override
{
    uint32_t timestamp;     /// Time when exercising is scheduled to run
    uint8_t mode        :3; /// \see #bt_location_maintenance_mode
} bt_location_exercising_schedule_override;


typedef struct PACK_BT_DATA bt_hc_mode_auto_switching_samples
{
    uint32_t next_sampling_period;	/// Time when next sampling may start (midnight of next day)
    uint16_t samples;				/// Bit-mask, each bit represents day, and is set when conditions to switch were fulfilled
} bt_hc_mode_auto_switching_samples;


typedef struct bt_location_outdoor_temp_filter_config
{
    uint32_t mode           :4; /// Filter mode (0 AVERAGE)
    uint32_t                :4; /// Reserved
    uint32_t length         :8; /// Number of samples (filter length)
    uint32_t suppression    :4; /// Filter suppression, x10 multiplied, range 0-10
    uint32_t sampling_rate  :12; /// Sampling rate (in minutes)
} bt_location_outdoor_temp_filter_config;

//-------------------------------------------------------------------------------------------------------------------------

#define BT_OUTDOOR_OUTDOOR_TEMP_BMS_OVERRIDE                    BT_VTPAIR( 0x8142, BT_VTYPE_D2_FP100)
#define BT_OUTDOOR_ERR_GENERAL_PROBLEM                          BT_VTPAIR( 0x403C, BT_VTYPE_JOINT_WARNING)
#define BT_OUTDOOR_PERIPH_WARN_LOW_BATTERY                      BT_VTPAIR( 0x403D, BT_VTYPE_JOINT_WARNING)
#define BT_OUTDOOR_PERIPH_WARN_UNREACHABLE                      BT_VTPAIR( 0x403E, BT_VTYPE_JOINT_WARNING)

//-------------------------------------------------------------------------------------------------------------------------

#define BT_DEV_SERIAL                                           BT_VTPAIR( 0x800C, BT_VTYPE_U4)
#define BT_DEV_SERIAL_PREFIX                                    BT_VTPAIR( 0x80DF, BT_VTYPE_U2)
#define BT_DEV_BL_CODE                                          BT_VTPAIR( 0x80E0, BT_VTYPE_U2)
#define BT_DEV_BL_VERSION                                       BT_VTPAIR( 0x80E1, BT_VTYPE_U1)
#define BT_DEV_BL_VERSION_MINOR                                 BT_VTPAIR( 0x80E2, BT_VTYPE_U1)
#define BT_DEV_HW_NAME                                          BT_VTPAIR( 0x80E3, BT_VTYPE_TEXT)
#define BT_DEV_HW_VERSION                                       BT_VTPAIR( 0x800E, BT_VTYPE_U1)
#define BT_DEV_SW_NAME                                          BT_VTPAIR( 0x80E4, BT_VTYPE_TEXT)
#define BT_DEV_SW_VARIANT                                       BT_VTPAIR( 0x80E5, BT_VTYPE_U1)
#define BT_DEV_SW_VERSION                                       BT_VTPAIR( 0x800D, BT_VTYPE_U1)
#define BT_DEV_SW_VERSION_MINOR                                 BT_VTPAIR( 0x809E, BT_VTYPE_U1)
#define BT_DEV_SW_VERSION_BRANCH                                BT_VTPAIR( 0x8135, BT_VTYPE_TEXT)
#define BT_DEV_CONFIG_VERSION                                   BT_VTPAIR( 0x848B, BT_VTYPE_U4)
#define BT_DEV_DESCR_VERSION                                    BT_VTPAIR( 0x84DC, BT_VTYPE_U1)
#define BT_DEV_STATUS                                           BT_VTPAIR( 0x2F  , BT_VTYPE_U4)
#define BT_DEV_MB_ADDR                                          BT_VTPAIR( 0x8001, BT_VTYPE_U1)
#define BT_DEV_ERR_BATTERY_OPEN                                 BT_VTPAIR( 0x4027, BT_VTYPE_WARNING)
#define BT_DEV_ERR_BADLY_INSTALLED                              BT_VTPAIR( 0x4028, BT_VTYPE_WARNING)
#define BT_DEV_WARN_LOW_BATERY                                  BT_VTPAIR( 0x4003, BT_VTYPE_WARNING)
#define BT_DEV_WARN_UNREACHABLE                                 BT_VTPAIR( 0x4004, BT_VTYPE_WARNING)
#define BT_DEV_WARN_PWR_FAIL                                    BT_VTPAIR( 0x4000, BT_VTYPE_WARNING)
#define BT_DEV_WARN_PWR_FAIL_30_MIN                             BT_VTPAIR( 0x4001, BT_VTYPE_WARNING)
#define BT_DEV_SIGNAL_STRENGTH                                  BT_VTPAIR( 0x73  , BT_VTYPE_D1)
#define BT_DEV_SIGNAL_STRENGTH_TX                               BT_VTPAIR( 0x74  , BT_VTYPE_D1)
#define BT_DEV_SIGNAL_STRENGTH_RX                               BT_VTPAIR( 0x75  , BT_VTYPE_D1)
#define BT_DEV_BATERY_LEVEL                                     BT_VTPAIR( 0x2C  , BT_VTYPE_U1)
#define BT_DEV_POWER_CONSUMERS_LIST                             BT_VTPAIR( 0x5A  , BT_VTYPE_DATA)
#define BT_DEV_OBJECT_LIST                                      BT_VTPAIR( 0x80B0, BT_VTYPE_DATA)
#define BT_DEV_PWR_STATIC_CURRENT                               BT_VTPAIR( 0x80B2, BT_VTYPE_U2)
#define BT_DEV_PWR_DYNAMIC_CURRENT_MIN                          BT_VTPAIR( 0x4E  , BT_VTYPE_U2)
#define BT_DEV_PWR_DYNAMIC_CURRENT_MAX                          BT_VTPAIR( 0x4D  , BT_VTYPE_U2)
#define BT_DEV_PWR_GRANTED_CURRENT                              BT_VTPAIR( 0x4F  , BT_VTYPE_U2)
#define BT_DEV_PWR_ACTUAL_CURRENT                               BT_VTPAIR( 0x50  , BT_VTYPE_U2)
#define BT_DEV_PWR_PRIORITY                                     BT_VTPAIR( 0x80B7, BT_VTYPE_ENUM)
#define BT_DEV_OWNER_ID                                         BT_VTPAIR( 0x80DE, BT_VTYPE_OID_REF)
#define BT_DEV_METADATA                                         BT_VTPAIR( 0x80FE, BT_VTYPE_DATA)
#define BT_DEV_SHUTDOWN                                         BT_VTPAIR( 0x66  , BT_VTYPE_ENUM)
#define BT_DEV_SHUTDOWN_TIME                                    BT_VTPAIR( 0x102 , BT_VTYPE_TIMESTAMP)
#define BT_DEV_CORRECTION_AIR_TEMP                              BT_VTPAIR( 0x811F, BT_VTYPE_TEMP)
#define BT_DEV_CORRECTION_FLOOR_TEMP                            BT_VTPAIR( 0x8120, BT_VTYPE_TEMP)
#define BT_DEV_CORRECTION_HUMIDITY                              BT_VTPAIR( 0x8121, BT_VTYPE_HUM)
#define BT_DEV_BRIGHTNESS_LOW_LIMIT                             BT_VTPAIR( 0x8122, BT_VTYPE_U1)
#define BT_DEV_BRIGHTNESS_HIGH_LIMIT                            BT_VTPAIR( 0x8123, BT_VTYPE_U1)
#define BT_DEV_TOUCH_SENSITIVITY                                BT_VTPAIR( 0x8124, BT_VTYPE_U1)
#define BT_DEV_THERM_HARD_LOCK                                  BT_VTPAIR( 0x808E, BT_VTYPE_U1)
#define BT_DEV_COM_RELIABILITY_TEST_DATA                        BT_VTPAIR( 0x0077, BT_VTYPE_DATA)
#define BT_DEV_UPDATE_CONTROL                                   BT_VTPAIR( 0x8067, BT_VTYPE_ENUM)
#define BT_DEV_UNDERVOLTAGE_LOCKOUT                             BT_VTPAIR( 0x402A, BT_VTYPE_U1)
#define BT_DEV_ERR_EXT_SENSOR_FAIL                              BT_VTPAIR( 0x4031, BT_VTYPE_WARNING)
#define BT_DEV_DEBUG_GROUP_MASK                                 BT_VTPAIR( 0x841F, BT_VTYPE_U4)
#define BT_DEV_BASE_TEMP                                        BT_VTPAIR( 0xA1  , BT_VTYPE_TEMP)
#define BT_DEV_ERR_VALVE_STICKED                                BT_VTPAIR( 0x404B, BT_VTYPE_WARNING)
#define BT_DEV_STATUS_FILTER                                    BT_VTPAIR( 0xBA  , BT_VTYPE_U1)
#define BT_DEV_ERR_INCOMPATIBLE_PERIPH                          BT_VTPAIR( 0x4051, BT_VTYPE_U1)
#define BT_DEV_INTERNAL_TEMP                                    BT_VTPAIR( 0x10B , BT_VTYPE_TEMP)
#define BT_DEV_INTERNAL_TEMP_HISTOGRAM                          BT_VTPAIR( 0x111 , BT_VTYPE_DATA)
#define BT_DEV_INTERNAL_OVERHEAT_TIME                           BT_VTPAIR( 0x112 , BT_VTYPE_U4)
#define BT_DEV_ERR_INTERNAL_FAILURE                             BT_VTPAIR( 0x4075, BT_VTYPE_U1)
#define BT_DEV_BROKER_FLASH_REWRITE_COUNT                       BT_VTPAIR( 0xED  , BT_VTYPE_U4)

// Special VID for ROXi testing
#define BT_DEV_TEST_PUBLISH                                     BT_VTPAIR( 0xA2  , BT_VTYPE_DATA)

// Data descriptor for test publish
#define TEST_PUBLISH_MAX_SIZE 252
struct bt_device_test_publish
{
    uint8_t command;
    uint8_t param;
    uint8_t tx_size;
    uint8_t rx_size;
// Test data
    uint8_t test_data[TEST_PUBLISH_MAX_SIZE];
};

// statistics of BROKER
#define BT_DEV_USED_BR_PT_LINES                                 BT_VTPAIR( 0x44, BT_VTYPE_U1)
#define BT_DEV_USED_BR_PT_MB                                    BT_VTPAIR( 0x45, BT_VTYPE_U1)
#define BT_DEV_USED_BR_IQ_PEAK                                  BT_VTPAIR( 0x46, BT_VTYPE_U1)
#define BT_DEV_USED_BR_IQP_PEAK                                 BT_VTPAIR( 0x47, BT_VTYPE_U1)
#define BT_DEV_USED_BR_SUBSCR                                   BT_VTPAIR( 0x48, BT_VTYPE_U1)
#define BT_DEV_USED_BR_CLIENTS                                  BT_VTPAIR( 0x49, BT_VTYPE_U1)

enum bt_device_shutdown
{
    BT_DEVICE_SHUTDOWN_REBOOT			= 1,
    BT_DEVICE_SHUTDOWN_SLAVE_UPGRADE_FW	= 2,
    BT_DEVICE_SHUTDOWN_FILE_UPGRADE_FW	= 3,
    BT_DEVICE_SHUTDOWN_FACTORY_CFG		= 4,
};

enum bt_device_status {
    BT_DEVICE_STATUS_ONLINE             = 0,
    BT_DEVICE_STATUS_BOOTLDR            = 1,
    BT_DEVICE_STATUS_RUNNING            = 2,
    BT_DEVICE_STATUS_SERVICE            = 3,
    BT_DEVICE_STATUS_LOST               = 0x100     // device lost timestamp 0x100 and above
};

enum bt_device_pwr_priority {
    BT_DEVICE_PWR_PRIORITY_LOW          = 0,
    BT_DEVICE_PWR_PRIORITY_MEDIUM       = 1,
    BT_DEVICE_PWR_PRIORITY_HIGH         = 2,
    BT_DEVICE_PWR_PRIORITY_REALTIME     = 3,
};

enum bt_device_update_control {
    BT_DEVICE_UPDATE_CONTROL_IGNORED,					// Set to all peripherals, that was unlearned before update
    BT_DEVICE_UPDATE_CONTROL_OFFLINE,					// Set to all peripherals, that was offline before update
    BT_DEVICE_UPDATE_CONTROL_UNCHECKED,					// Set to all peripherals prepared to check
    BT_DEVICE_UPDATE_CONTROL_UPDATE_NOT_AVAILABLE,		// Set to all peripherals with no new firmware ready (incliding offline)
    BT_DEVICE_UPDATE_CONTROL_UPDATE_AVAILABLE,			// Set to all peripherals ready to update with newer fw
    BT_DEVICE_UPDATE_CONTROL_FORCED_UPDATE_AVAILABLE,	// Set to all peripherals forced to update to any version
    BT_DEVICE_UPDATE_CONTROL_SUCCESSFULLY_UPDATED,		// Set to all successfully updated peripherals
    BT_DEVICE_UPDATE_CONTROL_UPDATE_FAILS,				// Set to all not successfully updated peripherals
};

struct bt_device_metadata
{
    uint8_t device_removed              : 1;
    uint8_t force_reset_to_defaults     : 1;
    uint8_t                             : 6;

    uint8_t offset;
};

enum bt_device_status_filter {
    BT_DEVICE_STATUS_FILTER_BOOT_LEARN,					// State after boot or peripheral learn.
    BT_DEVICE_STATUS_FILTER_RUNNING,					// Device is running
    BT_DEVICE_STATUS_FILTER_RUNNING_FILTERED,			// Device is not running less than timeout
    BT_DEVICE_STATUS_FILTER_NOT_FILTERED				// Device is not running more than timeout
};

enum bt_device_warn_low_battery
{
    BT_DEVICE_WARN_LOW_BATTERY_OK,
    BT_DEVICE_WARN_LOW_BATTERY_LOW,
    BT_DEVICE_WARN_LOW_BATTERY_EMPTY,
};


/**
 * This header is a minimum of what the device descriptor must have.
 *
 * #descr_version denounces descriptor version
 * #dev_type is type of device as defined by bt_dev_type_t
 * #proto_version is supported protocol version
 */
struct bt_device_descriptor_hdr
{
    uint8_t  dev_type;						// see bt_dev_type_t
    uint8_t  reserved;
};

struct bt_device_descriptor_v1
{
    struct bt_device_descriptor_hdr hdr;

    // Byte 2

    uint16_t addr_prefix;					// serial number prefix (e.g. 1530)
    uint32_t addr;							// serial number - unique device address

    // Byte 8

    // Bootloader info
    char     bl_code[2];
    uint8_t  bl_version;
    uint8_t  bl_version_minor;

    // Byte 12

    // Hardware info
    char     hw_name[5];					// e.g. "TM100"
    uint8_t  hw_version;

    // Byte 18

    // Software info
    char     sw_name[5];
    uint8_t  sw_variant;
    uint8_t  sw_version;					// release version
    uint8_t  sw_version_minor;				// beta version
};

//-------------------------------------------------------------------------------------------------------------------------

#define BT_NET_STATE                                            BT_VTPAIR( 0xAC  , BT_VTYPE_U1)
#define BT_NET_DNS_IP_ADDRESS                                   BT_VTPAIR( 0xB9  , BT_VTYPE_U4)
#define BT_NET_STATIC_DNS_IP_ADDRESS                            BT_VTPAIR( 0x8478, BT_VTYPE_U4)


enum bt_net_state {
    BT_NET_STATE_WAIT_LINK,					// Cable disconnected, link down
    BT_NET_STATE_WAIT_IP,					// Awaiting DHCP response
    BT_NET_STATE_IP_READY,					// IP configured (either static or dynamic from DHCP)
    BT_NET_STATE_CLOUD_READY,				// Cloud connection is ready
};


//-------------------------------------------------------------------------------------------------------------------------

#define BT_ROOM_MODE                                            BT_VTPAIR( 0x8004, BT_VTYPE_ENUM)
#define BT_ROOM_MODE_OVERRIDE                                   BT_VTPAIR( 0x8005, BT_VTYPE_ENUM)
#define BT_ROOM_MODE_OVERRIDE_END_TIME                          BT_VTPAIR( 0x8006, BT_VTYPE_U4)
#define BT_ROOM_THERM_ACCESS_LEVEL                              BT_VTPAIR( 0x8008, BT_VTYPE_U1)
#define BT_ROOM_THERM_HARD_LOCK                                 BT_VTPAIR( 0x808E, BT_VTYPE_U1)
#define BT_ROOM_SCHEDULE                                        BT_VTPAIR( 0x8043, BT_VTYPE_DATA)
#define BT_ROOM_ALLOW_VACATION_AWAY                             BT_VTPAIR( 0x8084, BT_VTYPE_U1)
#define BT_ROOM_ALLOW_COOLING                                   BT_VTPAIR( 0x8438, BT_VTYPE_U1)
#define BT_ROOM_OUTPUT_LIST                                     BT_VTPAIR( 0x808F, BT_VTYPE_DATA)
#define BT_ROOM_PERIPHERAL_LIST                                 BT_OBJECT_PERIPHERAL_LIST
#define BT_ROOM_COMFORT_LEVEL                                   BT_VTPAIR( 0x3C  , BT_VTYPE_ENUM)   // bt_week_schedule_interval
#define BT_ROOM_WARN_GENERAL_PROBLEM                            BT_VTPAIR( 0x4002, BT_VTYPE_JOINT_WARNING)
#define BT_ROOM_WARN_PERIPH_LOW_BATERY                          BT_VTPAIR( 0x400F, BT_VTYPE_JOINT_WARNING)
#define BT_ROOM_ALARM_PERIPH_UNREACHABLE                        BT_VTPAIR( 0x4010, BT_VTYPE_JOINT_WARNING)
#define BT_ROOM_ALARM_NO_TEMP_SOURCE                            BT_VTPAIR( 0x4019, BT_VTYPE_WARNING)
#define BT_ROOM_ALARM_OUTPUT_LOST                               BT_VTPAIR( 0x401A, BT_VTYPE_WARNING)
#define BT_ROOM_ALARM_OUTPUT_ERROR                              BT_VTPAIR( 0x401B, BT_VTYPE_WARNING)
#define BT_ROOM_ALARM_FROST_PROTECTION                          BT_VTPAIR( 0x402B, BT_VTYPE_WARNING)
#define BT_ROOM_ALARM_BATTERY_OPEN                              BT_VTPAIR( 0x4042, BT_VTYPE_WARNING)
#define BT_ROOM_ALARM_BADLY_INSTALLED                           BT_VTPAIR( 0x4043, BT_VTYPE_WARNING)
#define BT_ROOM_WARN_STICKING_VALVE                             BT_VTPAIR( 0x404C, BT_VTYPE_WARNING)
#define BT_ROOM_AGGREGATED_NON_AUTONOMOUS_SRT_AIR_TEMP          BT_VTPAIR( 0xAD  , BT_VTYPE_TEMP)
#define BT_ROOM_ERR_INCOMPATIBLE_PERIPH                         BT_VTPAIR( 0x4052, BT_VTYPE_U1)
#define BT_ROOM_ALARM_PERIPH_UNREACHABLE_FILTERED               BT_VTPAIR( 0x4053, BT_VTYPE_U1)
#define BT_ROOM_CTRL_CONFIG_MASK                                BT_VTPAIR( 0x84F4, BT_VTYPE_DATA)

enum bt_room_mode {
    BT_ROOM_MODE_SCHEDULE               = 0,
    BT_ROOM_MODE_MANUAL                 = 1,
};

enum bt_room_mode_override {
    BT_ROOM_MODE_OVERRIDE_NONE          = 0,
    BT_ROOM_MODE_OVERRIDE_PARTY         = 1,
    BT_ROOM_MODE_OVERRIDE_VACATION_AWAY = 2,
    BT_ROOM_MODE_OVERRIDE_ADJUST        = 3,
    BT_ROOM_MODE_OVERRIDE_MAX
};

enum bt_room_therm_access_level {
    BT_ROOM_THERM_ACCESS_LEVEL_OFF          = 0,
    BT_ROOM_THERM_ACCESS_LEVEL_READ_ONLY    = 8,
    BT_ROOM_THERM_ACCESS_LEVEL_USER_ADJUST  = 16,
    BT_ROOM_THERM_ACCESS_LEVEL_USER         = 24,
    BT_ROOM_THERM_ACCESS_LEVEL_MASTER       = 32,
    BT_ROOM_THERM_ACCESS_LEVEL_INSTALLER    = 40,
};

typedef struct
{
    union
    {
        uint32_t raw;

        struct
        {
            uint32_t hum_ctrl_threshold_standby_enable   :1;
            uint32_t hum_ctrl_threshold_vacation_enable  :1;
        } bits;
    };
} bt_room_ctrl_config_mask;


//-------------------------------------------------------------------------------------------------------------------------

/**
 *  \deprecated Aggregated values to be used by older LCD-200
 *  @{
 */
#define BT_TEMP_CTRL_STATE                                      BT_VTPAIR( 0x1B  , BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_BLOCKING                                   BT_VTPAIR( 0x1C  , BT_VTYPE_ENUM)
/**
 *  @}
 */

#define BT_TEMP_CTRL_RADIATOR_STATE                             BT_VTPAIR( 0xB3  , BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_RADIATOR_BLOCKING                          BT_VTPAIR( 0xB4  , BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_UFHC_STATE                                 BT_VTPAIR( 0xB5  , BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_UFHC_BLOCKING                              BT_VTPAIR( 0x9D  , BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_TEMP_DESIRED                               BT_VTPAIR( 0x1D  , BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_FLOOR_TEMP_DESIRED                         BT_VTPAIR( 0x9E  , BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_VALVE_LEVEL                                BT_VTPAIR( 0x38  , BT_VTYPE_PERCENT)
#define BT_TEMP_CTRL_PROPORTIONAL_LEVEL                         BT_VTPAIR( 0x67  , BT_VTYPE_PERCENT)
#define BT_TEMP_CTRL_UFHC_VALVE_LEVEL                           BT_TEMP_CTRL_VALVE_LEVEL
#define BT_TEMP_CTRL_UFHC_PROPORTIONAL_LEVEL                    BT_TEMP_CTRL_PROPORTIONAL_LEVEL
#define BT_TEMP_CTRL_UFHC_DEMAND                                BT_VTPAIR( 0xBB  , BT_VTYPE_PERCENT)
#define BT_TEMP_CTRL_RADIATOR_VALVE_LEVEL                       BT_VTPAIR( 0x6B  , BT_VTYPE_PERCENT)
#define BT_TEMP_CTRL_RADIATOR_PROPORTIONAL_LEVEL                BT_VTPAIR( 0x6C  , BT_VTYPE_PERCENT)
#define BT_TEMP_CTRL_RADIATOR_DEMAND                            BT_VTPAIR( 0x69  , BT_VTYPE_PERCENT)
#define BT_TEMP_CTRL_PROPORTIONAL_LEVEL_BAND                    BT_VTPAIR( 0x8128, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_PROPORTIONAL_BAND_OFFSET                   BT_VTPAIR( 0x8138, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_PROPORTIONAL_OUTPUT_OFFSET                 BT_VTPAIR( 0x813B, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_TEMP_ALARM_LOW                             BT_VTPAIR( 0x8010, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_TEMP_ALARM_HIGH                            BT_VTPAIR( 0x8011, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_FLOOR_TEMP_ALARM_LOW                       BT_VTPAIR( 0x80F3, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_FLOOR_TEMP_ALARM_HIGH                      BT_VTPAIR( 0x80F4, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_ALARM_LOW_TEMP                             BT_VTPAIR( 0x4005, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_ALARM_HIGH_TEMP                            BT_VTPAIR( 0x4006, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_ALARM_LOW_FLOOR_TEMP                       BT_VTPAIR( 0x4011, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_ALARM_HIGH_FLOOR_TEMP                      BT_VTPAIR( 0x4012, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_ERR_NO_UFHC_OUTPUT                         BT_VTPAIR( 0x404D, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_WARN_NO_UFHC_SUPPLIER                      BT_VTPAIR( 0x404E, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_WARN_NO_RADIATOR_SUPPLIER                  BT_VTPAIR( 0x404F, BT_VTYPE_WARNING)
#define BT_TEMP_CTRL_FLOOR_SRT_CONTROL                          BT_VTPAIR( 0x9F  , BT_VTYPE_DATA)
#define BT_TEMP_CTRL_RADIATOR_SRT_CONTROL                       BT_VTPAIR( 0xA0  , BT_VTYPE_DATA)
#define BT_TEMP_CTRL_COOPERATION_MODE_USED                      BT_VTPAIR( 0xAF  , BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_COOPERATION_MODE                           BT_VTPAIR( 0x847F, BT_VTYPE_ENUM)

#define BT_TEMP_CTRL_HEAT_REGULATED_VAL_SRC                     BT_VTPAIR( 0x8014, BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_HEAT_ADAPTIVE_MODE_ENA                     BT_VTPAIR( 0x8016, BT_VTYPE_ENUM)
#define BT_TEMP_CTRL_HEAT_TEMP_SPAN_MIN                         BT_VTPAIR( 0x8018, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SPAN_MAX                         BT_VTPAIR( 0x8019, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_MANUAL                       BT_VTPAIR( 0x801A, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_ECO                          BT_VTPAIR( 0x801B, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_COMFORT                      BT_VTPAIR( 0x801C, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_EXTRA_COMFORT                BT_VTPAIR( 0x801D, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_TEMPORARY                    BT_VTPAIR( 0x801E, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_VACATION                     BT_VTPAIR( 0x801F, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_ADJUSTED                     BT_VTPAIR( 0x8020, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_SET_STANDBY                      BT_VTPAIR( 0x8021, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_TEMP_HYSTERESIS                       BT_VTPAIR( 0x8022, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_HYSTERESIS                 BT_VTPAIR( 0x8078, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MIN                  BT_VTPAIR( 0x80A4, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MAX                  BT_VTPAIR( 0x8026, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MIN_ECO              BT_VTPAIR( 0x8023, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MIN_COMFORT          BT_VTPAIR( 0x8024, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MIN_EXTRA_COMFORT    BT_VTPAIR( 0x8025, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MAX_ECO              BT_VTPAIR( 0x8079, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MAX_COMFORT          BT_VTPAIR( 0x8080, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_FLOOR_TEMP_LIMIT_MAX_EXTRA_COMFORT    BT_VTPAIR( 0x8081, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_COOPERATION_NORMAL_DEADBAND           BT_VTPAIR( 0x847D, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_COOPERATION_INCREASED_DEADBAND        BT_VTPAIR( 0x847E, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_HEAT_ADAPTIVE_VALUES                       BT_VTPAIR( 0x8483, BT_VTYPE_DATA)

#define BT_TEMP_CTRL_COOL_TEMP_SPAN_MIN                         BT_VTPAIR( 0x802B, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SPAN_MAX                         BT_VTPAIR( 0x802C, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_MANUAL                       BT_VTPAIR( 0x802D, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_ECO                          BT_VTPAIR( 0x802E, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_COMFORT                      BT_VTPAIR( 0x802F, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_EXTRA_COMFORT                BT_VTPAIR( 0x8030, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_TEMPORARY                    BT_VTPAIR( 0x8031, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_VACATION                     BT_VTPAIR( 0x8032, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_ADJUSTED                     BT_VTPAIR( 0x8033, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_SET_STANDBY                      BT_VTPAIR( 0x8082, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_TEMP_HYSTERESIS                       BT_VTPAIR( 0x8034, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_FLOOR_TEMP_HYSTERESIS                 BT_VTPAIR( 0x8480, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_FLOOR_TEMP_LIMIT_MIN                  BT_VTPAIR( 0x8038, BT_VTYPE_TEMP)
#define BT_TEMP_CTRL_COOL_DEW_POINT_INTEGRATION_THRESHOLD       BT_VTPAIR( 0x8470, BT_VTYPE_U4)

enum bt_tmp_ctrl_state {
    BT_TMP_CTRL_STATE_OFF               = 0,//!< BT_TMP_CTRL_STATE_OFF
    BT_TMP_CTRL_STATE_IDLE              = 1,//!< BT_TMP_CTRL_STATE_IDLE
    BT_TMP_CTRL_STATE_HEATING           = 2,//!< BT_TMP_CTRL_STATE_HEATING
    BT_TMP_CTRL_STATE_COOLING           = 3,//!< BT_TMP_CTRL_STATE_COOLING
    BT_TMP_CTRL_STATE_MAX,
};

enum bt_tmp_ctrl_blocking {
    BT_TMP_CTRL_BLOCKING_NONE           = 0,
    BT_TMP_CTRL_BLOCKING_UNKNOWN        = 1,
    BT_TMP_CTRL_BLOCKING_CONTACT        = 2,
    BT_TMP_CTRL_BLOCKING_FLOOR          = 3,
    BT_TMP_CTRL_BLOCKING_LOW_ENERGY     = 4,
    BT_TMP_CTRL_BLOCKING_ALARM          = 5,
    BT_TMP_CTRL_BLOCKING_DEW_POINT      = 6,
    BT_TMP_CTRL_BLOCKING_MAX,
};

enum bt_tmp_ctrl_regulated_val_src {                    // NOTE: The same values for cooling and heating
    BT_TMP_CTRL_REGULATED_VAL_SRC_FLOOR             = 0,
    BT_TMP_CTRL_REGULATED_VAL_SRC_AIR               = 1,
    BT_TMP_CTRL_REGULATED_VAL_SRC_AIR_FLOOR_MAX     = 2,
    BT_TMP_CTRL_REGULATED_VAL_SRC_AIR_FLOOR_MAX_MIN = 3,
    BT_TMP_CTRL_REGULATED_VAL_SRC_NO_TEMP_SOURCES   = 4
};

enum bt_tmp_ctrl_cooperation_mode {
    BT_TMP_CTRL_COOPERATION_MODE_OFF                = 0,
    BT_TMP_CTRL_COOPERATION_MODE_NORMAL             = 1,
    BT_TMP_CTRL_COOPERATION_MODE_INCREASED          = 2,
};

typedef struct PACK_BT_DATA bt_tmp_ctrl_srt_control {
    uint8_t suppress_move    :1;  // Don't move, water not flowing
    uint8_t freezing         :1;  // Frost protection - Freezing
    uint8_t failure          :1;  // Frost protection - Failure, temperature not available
    uint8_t regulation_mode  :5;  // Room regulation mode
    uint8_t no_demand        :1;  // Room's supplier is active
    uint8_t value_src_enable :1;  // 1: disable internal regulator and override output by value source
    uint8_t                  :6;  // Filler
    uint8_t reserved[2];
} bt_tmp_ctrl_radiator_srt_control, bt_tmp_ctrl_floor_srt_control;


enum bt_tmp_ctrl_srt_control_regulation_mode {
    BT_TMP_CTRL_SRT_CONTROL_REGULATION_MODE_FLOOR                   = 0,
    BT_TMP_CTRL_SRT_CONTROL_REGULATION_MODE_AIR                     = 1,
    BT_TMP_CTRL_SRT_CONTROL_REGULATION_MODE_AIR_WITH_FLOOR_LIMIT    = 3,
};


typedef struct bt_tmp_ctrl_adapt_val {
    uint16_t heat_delay;
    uint16_t gradient;
} bt_tmp_ctrl_adapt_val;

//-------------------------------------------------------------------------------------------------------------------------

#define BT_INTEGRATION_CTRL_OFFSET                              BT_VTPAIR( 0x8435, BT_VTYPE_TEMP)
#define BT_INTEGRATION_CTRL_HYSTERESIS                          BT_VTPAIR( 0x8436, BT_VTYPE_TEMP)

//-------------------------------------------------------------------------------------------------------------------------

#define BT_HUM_CTRL_PROGRAMMABLE_OUTPUT_LEVEL                   BT_VTPAIR( 0x76  , BT_VTYPE_U1)
#define BT_HUM_CTRL_ALARM_HIGH_HUMIDITY                         BT_VTPAIR( 0x4007, BT_VTYPE_WARNING)
#define BT_HUM_CTRL_ENABLED                                     BT_VTPAIR( 0x8083, BT_VTYPE_ENUM)
#define BT_HUM_CTRL_THERMOSTAT_ADJUST_ENABLED                   BT_VTPAIR( 0x84EF, BT_VTYPE_BOOL)
#define BT_HUM_CTRL_HUM_SPAN_MIN                                BT_VTPAIR( 0x84F0, BT_VTYPE_HUM)
#define BT_HUM_CTRL_HUM_SPAN_MAX                                BT_VTPAIR( 0x84F1, BT_VTYPE_HUM)
#define BT_HUM_CTRL_HUM_HEAT_THRESHOLD                          BT_VTPAIR( 0x843B, BT_VTYPE_HUM)
#define BT_HUM_CTRL_HUM_COOL_THRESHOLD                          BT_VTPAIR( 0x8433, BT_VTYPE_HUM)
#define BT_HUM_CTRL_HUM_HYSTERESIS                              BT_VTPAIR( 0x803B, BT_VTYPE_HUM)
#define BT_HUM_CTRL_HUM_NIGHT_SETBACK_OFFSET                    BT_VTPAIR( 0x84F2, BT_VTYPE_HUM)
#define BT_HUM_CTRL_HUM_NIGHT_SETBACK_TIME_INTERVAL             BT_VTPAIR( 0x84F3, BT_VTYPE_DATA)
#define BT_HUM_CTRL_HUM_HEAT_DRYING_OFFSET                      BT_VTPAIR( 0x8434, BT_VTYPE_TEMP)
#define BT_HUM_CTRL_HUM_COOL_DRYING_OFFSET                      BT_VTPAIR( 0x843A, BT_VTYPE_TEMP)
#define BT_HUM_CTRL_HUM_DRYING_OFFSET_HYSTERESIS                BT_VTPAIR( 0x8437, BT_VTYPE_TEMP)
#define BT_HUM_CTRL_HUM_DRYING_ON_COOLING_DEW_POINT_THRESHOLD   BT_VTPAIR( 0x8440, BT_VTYPE_TEMP)
#define BT_HUM_CTRL_HUM_DRYING_ON_COOLING_DEW_POINT_HYSTERESIS  BT_VTPAIR( 0x8441, BT_VTYPE_TEMP)
#define BT_HUM_CTRL_HUM_ALARM_HIGH                              BT_VTPAIR( 0x803C, BT_VTYPE_HUM)


enum bt_hum_ctrl_enabled {
    BT_HUM_CTRL_ENABLED_DISABLED        = 0,
    BT_HUM_CTRL_ENABLED_OUTPUT          = 1,
    BT_HUM_CTRL_ENABLED_DEHUMIDIFIER    = 2,
    BT_HUM_CTRL_ENABLED_VENTILATION     = 3,
};

enum bt_hum_ctrl_state {
    BT_HUM_CTRL_STATE_IDLE              = 1,
    BT_HUM_CTRL_STATE_DRYING            = 3
};

enum bt_hum_ctrl_blocking {
    BT_HUM_CTRL_BLOCKING_NONE           = 0,
    BT_HUM_CTRL_BLOCKING_UNKNOWN        = 1,
    BT_HUM_CTRL_BLOCKING_CONTACT        = 2,
};


/**
 *  \deprecated Used by thermostats and LCD-200 in release 8 and lower.
 *
 *  In newer releases, the value is replaced with separated VIDs for heating/cooling:
 *  \li BT_HUM_CTRL_HUM_HEAT_THRESHOLD
 *  \li BT_HUM_CTRL_HUM_COOL_THRESHOLD
 *
 *  CCU synchronizes this value with the two values added:
 *  - When written into, it will copy the value into either heat/cool threshold
 *  - When heat/cool threshold is changed, this value is updated
 */
#define BT_HUM_CTRL_HUM_SET_MANUAL                              BT_VTPAIR( 0x803A, BT_VTYPE_HUM)


/**
 *  @deprecated Used in Sentio releases 8 and older
 *  @{
 */

#define BT_HUM_CTRL_STATE                                       BT_VTPAIR( 0x1E  , BT_VTYPE_ENUM)
#define BT_HUM_CTRL_BLOCKING                                    BT_VTPAIR( 0x1F  , BT_VTYPE_ENUM)

enum bt_hum_ctrl_enabled_deprecated {
    BT_HUM_CTRL_ENABLED_ENABLED         = 1,
};

/**
 * @}
 */

//-------------------------------------------------------------------------------------------------------------------------
// DHW
#define BT_DHW_STATE                                            BT_VTPAIR( 0x24  , BT_VTYPE_ENUM)
#define BT_DHW_BLOCKING                                         BT_VTPAIR( 0x25  , BT_VTYPE_ENUM)
#define BT_DHW_MODE                                             BT_VTPAIR( 0x8089, BT_VTYPE_ENUM)
#define BT_DHW_MODE_OVERRIDE                                    BT_VTPAIR( 0x808A, BT_VTYPE_ENUM)
#define BT_DHW_SCHEDULE                                         BT_VTPAIR( 0x808B, BT_VTYPE_DATA)
#define BT_DHW_ACCESS_LEVEL                                     BT_VTPAIR( 0x808C, BT_VTYPE_ENUM)
#define BT_DHW_WARN_GENERAL_PROBLEM                             BT_VTPAIR( 0x808C, BT_VTYPE_U1)
#define BT_DHW_ALLOW_VACATION_AWAY                              BT_VTPAIR( 0x808D, BT_VTYPE_U1)
#define BT_DHW_ALLOW_STANDBY                                    BT_VTPAIR( 0x8113, BT_VTYPE_U1)

//TANK
#define BT_DHW_TANK_CTRL_STATE                                  BT_VTPAIR( 0x60  , BT_VTYPE_ENUM)
#define BT_DHW_TANK_CTRL_TANK_TEMP                              BT_VTPAIR( 0x61  , BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_DESIRED                           BT_VTPAIR( 0x62  , BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_VALVE_LEVEL                            BT_VTPAIR( 0x7A  , BT_VTYPE_D2_FP100)
#define BT_DHW_TANK_CTRL_SERVO_REQUEST                          BT_VTPAIR( 0x78  , BT_VTYPE_PERCENT)
#define BT_DHW_TANK_CTRL_ERR_TANK_SENSOR_FAIL                   BT_VTPAIR( 0x4020, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_ERR_HCW_SOURCE_INLET_SENSOR_FAIL       BT_VTPAIR( 0x4039, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_WARN_CLEANING_FAIL                     BT_VTPAIR( 0x4021, BT_VTYPE_WARNING)
//#define BT_DHW_TANK_CTRL_ERR_HCW_SOURCE_RETURN_SENSOR_FAIL    BT_VTPAIR( 0x4029, BT_VTYPE_TEMP) // Wrong VTYPE assigned, deprecated
#define BT_DHW_TANK_CTRL_ERR_HCW_SOURCE_RETURN_SENSOR_FAIL      BT_VTPAIR( 0x403B, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_WARN_PERIPH_LOW_BATTERY                BT_VTPAIR( 0x4036, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_ERR_PERIPH_UNREACHABLE                 BT_VTPAIR( 0x4037, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_WARN_LOW_ENERGY                        BT_VTPAIR( 0x4038, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_WARN_LOW_HCW_SOURCE_TEMP               BT_VTPAIR( 0x403A, BT_VTYPE_WARNING)
#define BT_DHW_TANK_CTRL_TEMP_SET_MANUAL                        BT_VTPAIR( 0x8145, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_SET_ECO                           BT_VTPAIR( 0x8114, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_SET_COMFORT                       BT_VTPAIR( 0x8115, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_SET_STANDBY                       BT_VTPAIR( 0x8116, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_SET_VACATION                      BT_VTPAIR( 0x8117, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_SET_CLEANING                      BT_VTPAIR( 0x8118, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_HYSTERESIS                        BT_VTPAIR( 0x8119, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_CLEANING_ENABLE                        BT_VTPAIR( 0x8139, BT_VTYPE_U1)
#define BT_DHW_TANK_CTRL_CLEANING_INTERVAL                      BT_VTPAIR( 0x811A, BT_VTYPE_DATA)
#define BT_DHW_TANK_CTRL_CLEANING_PERIOD                        BT_VTPAIR( 0x811B, BT_VTYPE_U2)
#define BT_DHW_TANK_CTRL_CLEANING_TIME_BEFORE_FAIL              BT_VTPAIR( 0x811C, BT_VTYPE_U2)
#define BT_DHW_TANK_CTRL_LAST_CLEANING                          BT_VTPAIR( 0x8141, BT_VTYPE_U4)
#define BT_DHW_TANK_CTRL_TEMP_SPAN_MIN                          BT_VTPAIR( 0x811D, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_TEMP_SPAN_MAX                          BT_VTPAIR( 0x811E, BT_VTYPE_TEMP)
//#define BT_DHW_TANK_CTRL_ADVANCED_TANK                        BT_VTPAIR( 0x806D, BT_VTYPE_TEMP) // Wrong VTYPE assigned, deprecated
#define BT_DHW_TANK_CTRL_ADVANCED_TANK                          BT_VTPAIR( 0x814A, BT_VTYPE_TEMP)
#define BT_DHW_TANK_CTRL_HCW_SOURCE_RETURN_TEMP_LIMIT           BT_VTPAIR( 0x806E, BT_VTYPE_TEMP)

//CALEFA
#define BT_DHW_CALEFA_CTRL_TEMP_DESIRED                         BT_VTPAIR( 0x31  , BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_WARN_LOW_PRESS                       BT_VTPAIR( 0x4035, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_WARN_HIGH_PRESS                      BT_VTPAIR( 0x4034, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_WARN_LOW_ENERGY                      BT_VTPAIR( 0x4009, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_HIGH_TEMP                      BT_VTPAIR( 0x400A, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_DHI_SENSOR_FAIL                BT_VTPAIR( 0x4022, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_DHO_SENSOR_FAIL                BT_VTPAIR( 0x4023, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_DHW_SENSOR_FAIL                BT_VTPAIR( 0x4024, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_DCW_SENSOR_FAIL                BT_VTPAIR( 0x4025, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_MOTOR_FAIL                     BT_VTPAIR( 0x4026, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_ALARM_CRIT_LOW_PRESS                 BT_VTPAIR( 0x4033, BT_VTYPE_WARNING)
#define BT_DHW_CALEFA_CTRL_MODE                                 BT_VTPAIR( 0x8044, BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_PWR_LIMIT                            BT_VTPAIR( 0x809C, BT_VTYPE_U2)
#define BT_DHW_CALEFA_CTRL_TEMP_SPAN_MIN                        BT_VTPAIR( 0x8092, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_TEMP_SPAN_MAX                        BT_VTPAIR( 0x8093, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_TEMP_SET                             BT_VTPAIR( 0x8094, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_BYPASS_VALVE_PRESENT                 BT_VTPAIR( 0x33  , BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_BYPASS_SPAN_MIN                      BT_VTPAIR( 0x8097, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_BYPASS_SPAN_MAX                      BT_VTPAIR( 0x8098, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_BYPASS_SET                           BT_VTPAIR( 0x8099, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_DEFROST_MODE                         BT_VTPAIR( 0x8051, BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_DEFROST_TEMP                         BT_VTPAIR( 0x8052, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_BOOST_MODE                           BT_VTPAIR( 0x8049, BT_VTYPE_ENUM)
#define BT_DHW_CALEFA_CTRL_BOOST_STATE                          BT_VTPAIR( 0x34  , BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_BLOCK_BY_BMS                         BT_VTPAIR( 0x8127, BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_ENERGY_PRIORITY_MODE                 BT_VTPAIR( 0x8061, BT_VTYPE_ENUM)
#define BT_DHW_CALEFA_CTRL_ENERGY_PRIORITY_STATE                BT_VTPAIR( 0x2A  , BT_VTYPE_ENUM)
#define BT_DHW_CALEFA_CTRL_VALVE_LEVEL                          BT_VTPAIR( 0x2B  , BT_VTYPE_PERCENT)
#define BT_DHW_CALEFA_CTRL_FLOW_SENSOR_TYPE                     BT_VTPAIR( 0x848D, BT_VTYPE_ENUM)
#define BT_DHW_CALEFA_CTRL_ERR_PRESSURE                         BT_VTPAIR( 0x4073, BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_REG_MODE                             BT_VTPAIR( 0x109 , BT_VTYPE_ENUM)
#define BT_DHW_CALEFA_CTRL_DYNAMIC_MODE                         BT_VTPAIR( 0x84F5, BT_VTYPE_ENUM)
#define BT_DHW_CALEFA_CTRL_DYNAMIC_TIME                         BT_VTPAIR( 0x84F6, BT_VTYPE_U2)
#define BT_DHW_CALEFA_CTRL_DYNAMIC_SETPOINT                     BT_VTPAIR( 0x84F7, BT_VTYPE_TEMP)
#define BT_DHW_CALEFA_CTRL_ERR_FLOW_FAIL                        BT_VTPAIR( 0x4076, BT_VTYPE_U1)
#define BT_DHW_CALEFA_CTRL_HEX_FACTOR                           BT_VTPAIR( 0x84F8, BT_VTYPE_U2)
#define BT_DHW_CALEFA_CTRL_MOTOR_TEST_VAL                       BT_VTPAIR( 0x114 , BT_VTYPE_U2)
#define BT_DHW_CALEFA_CTRL_BACKUP_CHARGE_TIME                   BT_VTPAIR( 0x115 , BT_VTYPE_U2)

//CIRCULATION
#define BT_DHW_CIRC_CTRL_CIRC_PUMP_PRESENT                      BT_VTPAIR( 0x804E, BT_VTYPE_U1)
#define BT_DHW_CIRC_CTRL_RETURN_TEMP                            BT_VTPAIR( 0x30  , BT_VTYPE_TEMP)
#define BT_DHW_CIRC_CTRL_STATUS                                 BT_VTPAIR( 0x35  , BT_VTYPE_U1)
#define BT_DHW_CIRC_CTRL_ERR_CIRC_SENSOR_FAIL                   BT_VTPAIR( 0x400B, BT_VTYPE_WARNING)
#define BT_DHW_CIRC_CTRL_MODE                                   BT_VTPAIR( 0x804D, BT_VTYPE_U1)
#define BT_DHW_CIRC_CTRL_TEMP_SPAN_MIN                          BT_VTPAIR( 0x809A, BT_VTYPE_TEMP)
#define BT_DHW_CIRC_CTRL_TEMP_SPAN_MAX                          BT_VTPAIR( 0x809B, BT_VTYPE_TEMP)
#define BT_DHW_CIRC_CTRL_TEMP_SET                               BT_VTPAIR( 0x804F, BT_VTYPE_TEMP)
#define BT_DHW_CIRC_CTRL_TEMP_HYSTERESIS                        BT_VTPAIR( 0x8050, BT_VTYPE_TEMP)
#define BT_DHW_CIRC_CTRL_TEMP_DIFFERENCE                        BT_VTPAIR( 0x8148, BT_VTYPE_TEMP)
#define BT_DHW_CIRC_CTRL_COOLDOWN_TIME                          BT_VTPAIR( 0x8149, BT_VTYPE_U2)


//DHW HEAT

#define BT_DHW_HEAT_VALVE_LEVEL                                 BT_VTPAIR( 0x10C , BT_VTYPE_D2_FP100)
#define BT_DHW_HEAT_REG_MODE                                    BT_VTPAIR( 0x10D , BT_VTYPE_ENUM)
#define BT_DHW_HEAT_ERR_MOTOR_FAILURE                           BT_VTPAIR( 0x4074, BT_VTYPE_U1)
#define BT_DHW_HEAT_MOTOR_TEST_VAL                              BT_VTPAIR( 0x116 , BT_VTYPE_U2)
#define BT_DHW_HEAT_STATE                                       BT_VTPAIR( 0x117 , BT_VTYPE_ENUM)


enum bt_dhw_mode {
    BT_DHW_MODE_SCHEDULE                = 0,
    BT_DHW_MODE_SCHEDULE_ADAPTIVE       = 1,
    BT_DHW_MODE_ECO                     = 2,
    BT_DHW_MODE_COMFORT                 = 3,
};

enum bt_dhw_state {
    BT_DHW_STATE_IDLE                   = 0,
    BT_DHW_STATE_HEATING                = 1,
    BT_DHW_STATE_BYPASS                 = 2,
    BT_DHW_STATE_CLEANING               = 3,
    BT_DHW_STATE_SUPPRESSED             = 4,
};

enum bt_dhw_tank_state {
    BT_DHW_TANK_STATE_IDLE              = 0,
    BT_DHW_TANK_STATE_HEATING           = 1,
    BT_DHW_TANK_STATE_CLEANING          = 2,
};

enum bt_dhw_calefa_state {
    BT_DHW_CALEFA_STATE_IDLE            = 0,
    BT_DHW_CALEFA_STATE_HEATING         = 1,
    BT_DHW_CALEFA_STATE_BYPASS          = 2,
};

enum bt_dhw_calefa_boost_mode {
    BT_DHW_CALEFA_BOOST_MODE_OFF        = 0,
    BT_DHW_CALEFA_BOOST_MODE_LOW        = 1,
    BT_DHW_CALEFA_BOOST_MODE_HIGH       = 2,
};

enum bt_dhw_calefa_circ_mode {
    BT_DHW_CALEFA_CIRC_SCHEDULER        = 0,
    BT_DHW_CALEFA_CIRC_PERMANENT        = 1,
};

enum bt_dhw_calefa_energy_priority_mode {
	BT_DHW_CALEFA_ENERGY_PRIORITY_MODE_DISABLED	= 0,
	BT_DHW_CALEFA_ENERGY_PRIORITY_MODE_ENABLED	= 1,
};

enum bt_dhw_calefa_energy_priority_state {
	BT_DHW_CALEFA_ENERGY_PRIORITY_STATE_IDLE	= 0,
	BT_DHW_CALEFA_ENERGY_PRIORITY_STATE_ACTIVE	= 1,
};

enum bt_dhw_calefa_flow_sens_type {
    BT_DHW_CALEFA_FLOW_H210_DN8        = 0,
    BT_DHW_CALEFA_FLOW_H210_DN10       = 1,
};

enum bt_dhw_calefa_reg_mode {
    BT_DHW_CALEFA_REG_STARTUP               = 0,
    BT_DHW_CALEFA_REG_DIAGNOSTIC            = 1,
    BT_DHW_CALEFA_REG_FAILURE               = 2,
    BT_DHW_CALEFA_REG_AUTOMATIC             = 3,
    BT_DHW_CALEFA_REG_MANUAL                = 4,
    BT_DHW_CALEFA_REG_REMOTE                = 5,
    BT_DHW_CALEFA_REG_HEX_SEEK              = 6,
    BT_DHW_CALEFA_REG_MAX,
};

enum bt_dhw_calefa_dynamic_mode{
    BT_DHW_CALEFA_CTRL_MODE_CONSTANT        = 0,
    BT_DHW_CALEFA_CTRL_MODE_DYNAMIC         = 1,

};

enum bt_dhw_heat_reg_mode {
    BT_DHW_HEAT_REG_STARTUP               = 0,
    BT_DHW_HEAT_REG_DIAGNOSTIC            = 1,
    BT_DHW_HEAT_REG_FAILURE               = 2,
    BT_DHW_HEAT_REG_AUTOMATIC             = 3,
    BT_DHW_HEAT_REG_MANUAL                = 4,
    BT_DHW_HEAT_REG_REMOTE                = 5,
    BT_DHW_HEAT_REG_BLOCKED_BY_DHW        = 6,
    BT_DHW_HEAT_REG_MAX,
};

enum bt_dhw_heat_state {
    BT_DHW_HEAT_STATE_IDLE               = 0,
    BT_DHW_HEAT_STATE_HEATING            = 1,
};

//-------------------------------------------------------------------------------------------------------------------------
// ITC Object
#define BT_ITC_MODE                                             BT_VTPAIR( 0x8055, BT_VTYPE_ENUM )
//#define BT_ITC_HC_MODE                                          BT_VTPAIR( 0x8056, BT_VTYPE_ENUM )
#define BT_ITC_INLET_TEMP_DESIRED                               BT_VTPAIR( 0x3B  , BT_VTYPE_TEMP )
//#define BT_ITC_SRC_TEMP_DESIRED                                 BT_VTPAIR( 0x3A  , BT_VTYPE_TEMP )
//#define BT_ITC_SRC_DEMAND                                       BT_VTPAIR( 0x39  , BT_VTYPE_U1 )
#define BT_ITC_PUMP_DEMAND                                      BT_VTPAIR( 0x7C  , BT_VTYPE_U1 )
#define BT_ITC_WARN_LOW_ENERGY_HEAT                             BT_VTPAIR( 0x400C, BT_VTYPE_WARNING )
#define BT_ITC_WARN_LOW_ENERGY_COOL                             BT_VTPAIR( 0x400D, BT_VTYPE_WARNING )
#define BT_ITC_ERR_HTCO                                         BT_VTPAIR( 0x400E, BT_VTYPE_WARNING )
#define BT_ITC_ERR_REGULATOR_FAILURE                            BT_VTPAIR( 0x4017, BT_VTYPE_WARNING )
#define BT_ITC_WARN_REGULATION_LIMITED                          BT_VTPAIR( 0x4018, BT_VTYPE_WARNING )
#define BT_ITC_ERR_INLET_SENSOR_FAILURE                         BT_VTPAIR( 0x402D, BT_VTYPE_WARNING )
#define BT_ITC_ERR_SERVO_FAILURE                                BT_VTPAIR( 0x402E, BT_VTYPE_WARNING )
#define BT_ITC_ERR_RETURN_SENSOR_FAILURE                        BT_VTPAIR( 0x402F, BT_VTYPE_WARNING )
#define BT_ITC_ERR_OUTDOOR_SENSOR_FAILURE                       BT_VTPAIR( 0x4030, BT_VTYPE_WARNING )
#define BT_ITC_ERR_FROST_PROTECTION_ACTIVE                      BT_VTPAIR( 0x4032, BT_VTYPE_WARNING )
#define BT_ITC_CONSUMERS_LIST                                   BT_VTPAIR( 0x80B8, BT_VTYPE_DATA )
//#define BT_ITC_PUMP_ACT_MODE                                    BT_VTPAIR( 0x80B9, BT_VTYPE_U1 )
//#define BT_ITC_PUMP_ACT_IDLE                                    BT_VTPAIR( 0x80BA, BT_VTYPE_U1 )
//#define BT_ITC_PUMP_ACT_TIME                                    BT_VTPAIR( 0x80BB, BT_VTYPE_U1 )
//#define BT_ITC_PUMP_DELAY_START                                 BT_VTPAIR( 0x80BC, BT_VTYPE_U1 )
//#define BT_ITC_PUMP_DELAY_STOP                                  BT_VTPAIR( 0x80BD, BT_VTYPE_U1 )
#define BT_ITC_VALVE_ACT_MODE                                   BT_VTPAIR( 0x80BE, BT_VTYPE_U1 )
#define BT_ITC_VALVE_ACT_IDDLE                                  BT_VTPAIR( 0x80BF, BT_VTYPE_U1 )
#define BT_ITC_VALVE_ACT_CYCLES                                 BT_VTPAIR( 0x80C0, BT_VTYPE_U1 )
//#define BT_ITC_HEATING_SERIAL_MODE                              BT_VTPAIR( 0x80C1, BT_VTYPE_U1 )
#define BT_ITC_VALVE_STATUS                                     BT_VTPAIR( 0x40  , BT_VTYPE_U1 )
#define BT_ITC_PUMP_STATUS                                      BT_VTPAIR( 0x41  , BT_VTYPE_U1 )
#define BT_ITC_DESIRED_ROOM_TEMP                                BT_VTPAIR( 0x29   , BT_VTYPE_TEMP )
#define BT_ITC_ACTUAL_INLET_TEMP                                BT_VTPAIR( 0x3E   , BT_VTYPE_TEMP )
#define BT_ITC_ACTUAL_RETURN_TEMP                               BT_VTPAIR( 0x3F   , BT_VTYPE_TEMP )
#define BT_ITC_SERVO_REQUEST                                    BT_VTPAIR( 0x5B   , BT_VTYPE_PERCENT )

//ITC Heating controller+

#define BT_ITC_HTCO_MODE                                        BT_VTPAIR( 0x8057 , BT_VTYPE_U1 )
#define BT_ITC_HTCO_TEMP                                        BT_VTPAIR( 0x8059 , BT_VTYPE_TEMP )
#define BT_ITC_HTCO_INTEGRATION_THRESHOLD                       BT_VTPAIR( 0x8471 , BT_VTYPE_U4)
#define BT_ITC_HOCT_TEMP                                        BT_VTPAIR( 0x80C3 , BT_VTYPE_TEMP )
#define BT_ITC_REG_MODE                                         BT_VTPAIR( 0x805F , BT_VTYPE_ENUM )
#define BT_ITC_TEMP_SET_MANUAL                                  BT_VTPAIR( 0x8062 , BT_VTYPE_TEMP )
#define BT_ITC_MIN_INLET_TEMP                                   BT_VTPAIR( 0x8063 , BT_VTYPE_TEMP )
#define BT_ITC_MAX_INLET_TEMP                                   BT_VTPAIR( 0x8064 , BT_VTYPE_TEMP )
#define BT_ITC_CURVE                                            BT_VTPAIR( 0x3D ,   BT_VTYPE_D2_FP10 )
#define BT_ITC_P_DISPLACE                                       BT_VTPAIR( 0x8066 , BT_VTYPE_TEMP )
#define BT_ITC_NO_TS_GAIN                                       BT_VTPAIR( 0x80C4 , BT_VTYPE_D2_FP10 )
#define BT_ITC_CURVE_DESIGN_INLET                               BT_VTPAIR( 0x80C5 , BT_VTYPE_TEMP )
#define BT_ITC_CURVE_DESIGN_ROOM                                BT_VTPAIR( 0x80C6 , BT_VTYPE_TEMP )
#define BT_ITC_CURVE_DESIGN_OUTDOOR                             BT_VTPAIR( 0x80C7 , BT_VTYPE_TEMP )
#define BT_ITC_CURVE_TYPE                                       BT_VTPAIR( 0x80C8 , BT_VTYPE_ENUM )
#define BT_ITC_CURVE_MANUAL                                     BT_VTPAIR( 0x80C9 , BT_VTYPE_D2_FP10 )
#define BT_ITC_R_LIMIT_MODE                                     BT_VTPAIR( 0x80CA , BT_VTYPE_U1 )
#define BT_ITC_MAX_RETURN_TEMP                                  BT_VTPAIR( 0x80CB , BT_VTYPE_TEMP )
#define BT_ITC_MIN_RETURN_TEMP                                  BT_VTPAIR( 0x80CC , BT_VTYPE_TEMP )
#define BT_ITC_MAX_R_LIMIT_GAIN                                 BT_VTPAIR( 0x80CD , BT_VTYPE_D2_FP10 )
#define BT_ITC_MIN_R_LIMIT_GAIN                                 BT_VTPAIR( 0x80CE , BT_VTYPE_D2_FP10 )
#define BT_ITC_MIN_R_LIMIT_PRIOR                                BT_VTPAIR( 0x80DB , BT_VTYPE_U1 )
#define BT_ITC_BOOST_MODE                                       BT_VTPAIR( 0x80CF , BT_VTYPE_U1 )
#define BT_ITC_BOOST_LEVEL                                      BT_VTPAIR( 0x80D0 , BT_VTYPE_U1 )
#define BT_ITC_RAMPING_MODE                                     BT_VTPAIR( 0x80D1 , BT_VTYPE_U1 )
#define BT_ITC_RAMPING_TIME                                     BT_VTPAIR( 0x80D2 , BT_VTYPE_U1 )
#define BT_ITC_MAX_ROOM_COR_GAIN                                BT_VTPAIR( 0x80D3 , BT_VTYPE_D2_FP10 )
#define BT_ITC_MIX_ROOM_COR_GAIN                                BT_VTPAIR( 0x80D4 , BT_VTYPE_D2_FP10 )
#define BT_ITC_FROST_PROTECT_MODE                               BT_VTPAIR( 0x80D5 , BT_VTYPE_U1 )
#define BT_ITC_FROST_PROTECT_TEMP                               BT_VTPAIR( 0x80D6 , BT_VTYPE_TEMP )
#define BT_ITC_P_GAIN                                           BT_VTPAIR( 0x80D7 , BT_VTYPE_D2_FP10 )
#define BT_ITC_I_TIME                                           BT_VTPAIR( 0x80D8 , BT_VTYPE_U2 )
#define BT_ITC_HYSTERESIS                                       BT_VTPAIR( 0x80D9 , BT_VTYPE_TEMP )
#define BT_ITC_REQUIRED_SRC_TEMP_OFFSET                         BT_VTPAIR( 0x80C2, BT_VTYPE_TEMP )

//ITC Cooling controller
#define BT_ITC_COOL_P_GAIN                                      BT_VTPAIR( 0x846A , BT_VTYPE_D2_FP10 )
#define BT_ITC_COOL_I_TIME                                      BT_VTPAIR( 0x846B , BT_VTYPE_U2 )
#define BT_ITC_COOL_HYSTERESIS                                  BT_VTPAIR( 0x846C , BT_VTYPE_TEMP )
#define BT_ITC_COOL_MIN_INLET_TEMP                              BT_VTPAIR( 0x846D , BT_VTYPE_TEMP )
#define BT_ITC_COOL_MAX_INLET_TEMP                              BT_VTPAIR( 0x846E , BT_VTYPE_TEMP )
#define BT_ITC_COOL_REQUIRED_SRC_TEMP_OFFSET                    BT_VTPAIR( 0x846F,  BT_VTYPE_TEMP )


enum itc_regulator_mode
{
    ITC_REGULATOR_MANUAL,
    ITC_REGULATOR_EQUITHERM = 0
};

enum itc_heat_curve_type
{
    ITC_HEAT_CURVE_TYPE_MANUAL = 0,
    ITC_HEAT_CURVE_TYPE_CALCULATED,
    ITC_HEAT_CURVE_TYPE_UNDER_FLOOR_HEATING,
    ITC_HEAT_CURVE_TYPE_RADIATORS,
    ITC_HEAT_CURVE_TYPE_AUTOMATIC,
};

enum itc_return_temp_mode
{
    RETURN_TEMP_LIMIT_OFF = 0,
    RETURN_TEMP_LIMIT_MIN,
    RETURN_TEMP_LIMIT_MAX
};


//-------------------------------------------------------------------------------------------------------------------------

#define BT_HCC_MODE                                             BT_VTPAIR( 0x80FA, BT_VTYPE_U1)

#define BT_HCC_SRC_DEMAND                                       BT_VTPAIR( 0x53  , BT_VTYPE_U1 )
#define BT_HCC_PUMP_DEMAND                                      BT_VTPAIR( 0x7B  , BT_VTYPE_U1 )
#define BT_HCC_INLET_TEMP_DESIRED                               BT_VTPAIR( 0xBF  , BT_VTYPE_TEMP )
#define BT_HCC_ROOM_TEMP_DESIRED                                BT_VTPAIR( 0x54  , BT_VTYPE_TEMP )
#define BT_HCC_PUMP_STATUS                                      BT_VTPAIR( 0x55  , BT_VTYPE_U1 )

#define BT_HCC_STATE                                            BT_VTPAIR( 0x65  , BT_VTYPE_U1 )
#define BT_HCC_ERR_INLET_SENSOR_FAIL                            BT_VTPAIR( 0x401E, BT_VTYPE_WARNING )
#define BT_HCC_ERR_HTCO                                         BT_VTPAIR( 0x401F, BT_VTYPE_WARNING )
#define BT_HCC_HTCO_MODE                                        BT_VTPAIR( 0x80F9, BT_VTYPE_U1)
#define BT_HCC_HTCO_TEMP                                        BT_VTPAIR( 0x80F6, BT_VTYPE_TEMP)
#define BT_HCC_HTCO_TEMP_RELATIVE                               BT_VTPAIR( 0x8101, BT_VTYPE_TEMP )
#define BT_HCC_HTCO_INTEGRATION_THRESHOLD                       BT_VTPAIR( 0x8477, BT_VTYPE_U4)
#define BT_HCC_MIN_INLET_TEMP                                   BT_VTPAIR( 0x8102, BT_VTYPE_TEMP )
#define BT_HCC_MAX_INLET_TEMP                                   BT_VTPAIR( 0x8103, BT_VTYPE_TEMP )
#define BT_HCC_CURVE_TYPE                                       BT_VTPAIR( 0x8104, BT_VTYPE_ENUM )
#define BT_HCC_CURVE                                            BT_VTPAIR( 0x56  , BT_VTYPE_D2_FP10 )
#define BT_HCC_CURVE_MANUAL                                     BT_VTPAIR( 0x8105, BT_VTYPE_D2_FP10 )
#define BT_HCC_PARALLEL_DISP                                    BT_VTPAIR( 0x8106, BT_VTYPE_TEMP )
#define BT_HCC_CURVE_DESIGN_INLET                               BT_VTPAIR( 0x8107, BT_VTYPE_TEMP )
#define BT_HCC_CURVE_DESIGN_ROOM                                BT_VTPAIR( 0x8108, BT_VTYPE_TEMP )
#define BT_HCC_CURVE_DESIGN_OUTDOOR                             BT_VTPAIR( 0x8109, BT_VTYPE_TEMP )
#define BT_HCC_NO_TS_GAIN                                       BT_VTPAIR( 0x810A, BT_VTYPE_D2_FP10 )
#define BT_HCC_HOCT_TEMP                                        BT_VTPAIR( 0x810B, BT_VTYPE_TEMP )
#define BT_HCC_INLET_TEMP_SOURCE                                BT_VTPAIR( 0x8460, BT_VTYPE_DATA )
#define BT_HCC_ASSOCIATED_PUMP                                  BT_VTPAIR( 0x8462, BT_VTYPE_U4 )
#define BT_HCC_SERVO_REQUEST                                    BT_VTPAIR( 0x10E , BT_VTYPE_D2_FP100 )


enum hcc_state
{
    BT_HCC_STATE_IDLE = 0,
    BT_HCC_STATE_HEATING,
    BT_HCC_STATE_COOLING,
};

enum hcc_mode
{
    BT_HCC_MODE_ON_OFF = 0,
    BT_HCC_MODE_PROPORTIONAL,
};

enum hcc_htco_mode
{
    BT_HCC_HTCO_MODE_DISABLED = 0,
    BT_HCC_HTCO_MODE_ENABLED,
};

enum hcc_mode_heat_curve_type
{
    BT_HCC_HEAT_CURVE_TYPE_MANUAL = 0,
    BT_HCC_HEAT_CURVE_TYPE_CALCULATED,
    BT_HCC_HEAT_CURVE_TYPE_UNDER_FLOOR_HEATING,
    BT_HCC_HEAT_CURVE_TYPE_RADIATORS,
};


//-------------------------------------------------------------------------------------------------------------------------

// Interface
#define BT_EDEV_MODBUS_SLAVE_ID                                 BT_VTPAIR( 0x84B6, BT_VTYPE_U1)

// Maintenance
#define BT_EDEV_WARN_MAINTENANCE_ENDS_SOON                      BT_VTPAIR( 0x4072, BT_VTYPE_ENUM)
#define BT_EDEV_MAINTENANCE_STATE                               BT_VTPAIR( 0xEE  , BT_VTYPE_ENUM)
#define BT_EDEV_MAINTENANCE_REQUEST                             BT_VTPAIR( 0xEF  , BT_VTYPE_ENUM)

// Alarms
#define BT_EDEV_ERR_DEVICE_SPECIFIC                             BT_VTPAIR( 0x406E, BT_VTYPE_U4)
#define BT_EDEV_WARN_DEVICE_SPECIFIC                            BT_VTPAIR( 0x406F, BT_VTYPE_U4)
#define BT_EDEV_DEVICE_SPECIFIC_ERR_ACK                         BT_VTPAIR( 0xE5  , BT_VTYPE_ENUM)
#define BT_EDEV_DEVICE_SPECIFIC_WARN_ACK                        BT_VTPAIR( 0xE6  , BT_VTYPE_ENUM)

#define BT_EDEV_MVDI_ERR_DEVICE_FAULT                           BT_VTPAIR( 0x403F, BT_VTYPE_WARNING)
#define BT_EDEV_MVDI_ERR_NO_HCW_SUPPLIER                        BT_VTPAIR( 0x4040, BT_VTYPE_WARNING)
#define BT_EDEV_MVDI_WARN_REPLACE_AIR_FILTER                    BT_VTPAIR( 0x4041, BT_VTYPE_WARNING)

// Air filter
#define BT_EDEV_MVDI_AIR_FILTER_LIFETIME                        BT_VTPAIR( 0x8426, BT_VTYPE_U4)
#define BT_EDEV_MVDI_AIR_FILTER_LIFETIME_USED                   BT_VTPAIR( 0x8427, BT_VTYPE_U4)
#define BT_EDEV_MVDI_AIR_FILTER_LAST_CHANGE                     BT_VTPAIR( 0x843F, BT_VTYPE_TIMESTAMP)

// Drying and Integration
#define BT_EDEV_MVDI_DRYING_REQUIRED_HCW_TEMP                   BT_VTPAIR( 0x843C, BT_VTYPE_TEMP)
#define BT_EDEV_MVDI_INTEGRATION_HEAT_REQUIRED_HCW_TEMP         BT_VTPAIR( 0x843D, BT_VTYPE_TEMP)
#define BT_EDEV_MVDI_INTEGRATION_COOL_REQUIRED_HCW_TEMP         BT_VTPAIR( 0x843E, BT_VTYPE_TEMP)

#define BT_EDEV_MVDI_DRYING_ALLOW_MODE                          BT_VTPAIR( 0x842B, BT_VTYPE_ENUM)

#define BT_EDEV_MVDI_INTEGRATION_ALLOW_MODE                     BT_VTPAIR( 0x842C, BT_VTYPE_ENUM)
#define BT_EDEV_MVDI_INTEGRATION_DEMAND_CONDITION               BT_VTPAIR( 0x842D, BT_VTYPE_ENUM)
#define BT_EDEV_MVDI_INTEGRATION_DEMAND_ROOM_OID                BT_VTPAIR( 0x848C, BT_VTYPE_U4)

// Output signals
#define BT_EDEV_MVDI_PUMP_DEMAND                                BT_VTPAIR( 0x8E  , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_EXTA_DEMAND                                BT_VTPAIR( 0x8F  , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_DRYING_DEMAND                              BT_VTPAIR( 0x90  , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_INTEGRATION_DEMAND                         BT_VTPAIR( 0x91  , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_VENTILATION_DEMAND                         BT_VTPAIR( 0x92  , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_BYPASS_DAMPER_DEMAND                       BT_VTPAIR( 0xE9  , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_FAN_UNOCCUPIED_DEMAND                      BT_VTPAIR( 0x119 , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_FAN_ECO_DEMAND                             BT_VTPAIR( 0x11A , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_FAN_COMFORT_DEMAND                         BT_VTPAIR( 0x11B , BT_VTYPE_D2_FP100)
#define BT_EDEV_MVDI_FAN_BOOST_DEMAND                           BT_VTPAIR( 0x11C , BT_VTYPE_D2_FP100)


enum bt_edev_maintenance_state {
    BT_EDEV_MAINTENANCE_STATE_INACTIVE = 0,         // No maintenance is needed
    BT_EDEV_MAINTENANCE_STATE_REQUIRED,             // Device requires maintenance
    BT_EDEV_MAINTENANCE_STATE_AWAITING_TIMED,       // Device has stopped temporarily for maintenance
};

enum bt_edev_maintenance_request {
    BT_EDEV_MAINTENANCE_REQUEST_NONE = 0,           // No request
    BT_EDEV_MAINTENANCE_REQUEST_STOP_OPERATION,     // Stop device
    BT_EDEV_MAINTENANCE_REQUEST_RESUME_OPERATION,   // Resume normal operation
    BT_EDEV_MAINTENANCE_REQUEST_RESET_AIR_FILTER,   // Reset Air Filter lifetime and time of replacement
};

enum bt_edev_device_specific_alarm_ack {
    BT_EDEV_DEVICE_SPECIFIC_ALARM_ACK_NONE = 0,
    BT_EDEV_DEVICE_SPECIFIC_ALARM_ACK_ACKNOWLEDGE_REQUIRED,
    BT_EDEV_DEVICE_SPECIFIC_ALARM_ACK_ACKNOWLEDGED,
    BT_EDEV_DEVICE_SPECIFIC_ALARM_ACK_RESET_REQUIRED,
    BT_EDEV_DEVICE_SPECIFIC_ALARM_ACK_RESET,
};

enum edev_mvdi_warn_replace_air_filter {
    BT_EDEV_MVDI_WARN_REPLACE_AIR_FILTER_OFF = 0,
    BT_EDEV_MVDI_WARN_REPLACE_AIR_FILTER_LIFETIME_USED = 1,
    BT_EDEV_MVDI_WARN_REPLACE_AIR_FILTER_SOLAR_YEAR = 2,
};

enum bt_edev_mvdi_err_device_fault {
    BT_EDEV_MVDI_ERR_DEVICE_FAULT_NONE = 0,
    BT_EDEV_MVDI_ERR_DEVICE_FAULT_GENERAL_PROBLEM,
    BT_EDEV_MVDI_ERR_DEVICE_FAULT_COMMUNICATION,
    BT_EDEV_MVDI_ERR_DEVICE_FAULT_INCOMPATIBLE,
};

enum drying_allow_mode {
    BT_EDEV_MVDI_DRYING_ALLOW_MODE_COOLING = 0,
    BT_EDEV_MVDI_DRYING_ALLOW_MODE_HEATING,
    BT_EDEV_MVDI_DRYING_ALLOW_MODE_BOTH,
};

enum integration_allow_mode {
    BT_EDEV_MVDI_INTEGRATION_ALLOW_MODE_COOLING = 0,
    BT_EDEV_MVDI_INTEGRATION_ALLOW_MODE_HEATING,
    BT_EDEV_MVDI_INTEGRATION_ALLOW_MODE_BOTH,
};

enum integration_demand_condition {
    BT_EDEV_MVDI_INTEGRATION_DEMAND_ANY_ROOM = 0,
    BT_EDEV_MVDI_INTEGRATION_DEMAND_ALL_ROOMS,
};


//-------------------------------------------------------------------------------------------------------------------------

#define BT_EDEV_CMV_DEVICE_STATE                                BT_VTPAIR( 0xF8  , BT_VTYPE_ENUM)
#define BT_EDEV_CMV_DEVICE_MANUFACTURER                         BT_VTPAIR( 0xFB  , BT_VTYPE_TEXT)
#define BT_EDEV_CMV_DEVICE_MODEL                                BT_VTPAIR( 0xFC  , BT_VTYPE_TEXT)
#define BT_EDEV_CMV_DEVICE_FEATURES                             BT_VTPAIR( 0x101 , BT_VTYPE_U4)
#define BT_EDEV_CMV_DEVICE_FEATURES_ENABLED                     BT_VTPAIR( 0x118 , BT_VTYPE_U4)
#define BT_EDEV_CMV_DEVICE_IDENTIFICATION_STRATEGY              BT_VTPAIR( 0x84DB, BT_VTYPE_U1)

#define BT_EDEV_CMV_FAN_SPEED_SUPPLY                            BT_VTPAIR( 0xE7  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_FAN_SPEED_EXHAUST                           BT_VTPAIR( 0xE8  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_SUPPLY_VOLUME_FLOW                          BT_VTPAIR( 0xF3  , BT_VTYPE_D2)
#define BT_EDEV_CMV_EXHAUST_VOLUME_FLOW                         BT_VTPAIR( 0xF4  , BT_VTYPE_D2)
#define BT_EDEV_CMV_BYPASS_DAMPER_POSITION                      BT_VTPAIR( 0xEB  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_AIR_TEMP_INTAKE                             BT_VTPAIR( 0xE1  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_AIR_TEMP_SUPPLY                             BT_VTPAIR( 0xE2  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_AIR_TEMP_EXTRACT                            BT_VTPAIR( 0xE3  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_AIR_TEMP_EXHAUST                            BT_VTPAIR( 0xE4  , BT_VTYPE_D2_FP100)
#define BT_EDEV_CMV_FREE_COOLING_ENABLED                        BT_VTPAIR( 0xF9  , BT_VTYPE_ENUM)

#define BT_EDEV_CMV_EXHAUST_FAN_MIN_PERCENT                     BT_VTPAIR( 0x84FA, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_EXHAUST_FAN_MAX_PERCENT                     BT_VTPAIR( 0x84FB, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_UNOCCUPIED_PERCENT        BT_VTPAIR( 0x84A7, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_ECO_PERCENT               BT_VTPAIR( 0x84A8, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_COMFORT_PERCENT           BT_VTPAIR( 0x84A9, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_BOOST_PERCENT             BT_VTPAIR( 0x84AA, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_EXHAUST_FAN_MIN_VOLUME                      BT_VTPAIR( 0x84D2, BT_VTYPE_D2)
#define BT_EDEV_CMV_EXHAUST_FAN_MAX_VOLUME                      BT_VTPAIR( 0x84D0, BT_VTYPE_D2)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_UNOCCUPIED_VOLUME         BT_VTPAIR( 0x84C8, BT_VTYPE_D2)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_ECO_VOLUME                BT_VTPAIR( 0x84C9, BT_VTYPE_D2)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_COMFORT_VOLUME            BT_VTPAIR( 0x84CA, BT_VTYPE_D2)
#define BT_EDEV_CMV_EXHAUST_FAN_LEVEL_BOOST_VOLUME              BT_VTPAIR( 0x84CB, BT_VTYPE_D2)

#define BT_EDEV_CMV_SUPPLY_FAN_MIN_PERCENT                      BT_VTPAIR( 0x84FC, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_SUPPLY_FAN_MAX_PERCENT                      BT_VTPAIR( 0x84FD, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_UNOCCUPIED_PERCENT         BT_VTPAIR( 0x84BB, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_ECO_PERCENT                BT_VTPAIR( 0x84BC, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_COMFORT_PERCENT            BT_VTPAIR( 0x84BD, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_BOOST_PERCENT              BT_VTPAIR( 0x84BE, BT_VTYPE_PERCENT)
#define BT_EDEV_CMV_SUPPLY_FAN_MIN_VOLUME                       BT_VTPAIR( 0x84D3, BT_VTYPE_D2)
#define BT_EDEV_CMV_SUPPLY_FAN_MAX_VOLUME                       BT_VTPAIR( 0x84D1, BT_VTYPE_D2)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_UNOCCUPIED_VOLUME          BT_VTPAIR( 0x84CC, BT_VTYPE_D2)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_ECO_VOLUME                 BT_VTPAIR( 0x84CD, BT_VTYPE_D2)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_COMFORT_VOLUME             BT_VTPAIR( 0x84CE, BT_VTYPE_D2)
#define BT_EDEV_CMV_SUPPLY_FAN_LEVEL_BOOST_VOLUME               BT_VTPAIR( 0x84CF, BT_VTYPE_D2)

#define BT_EDEV_CMV_SCHEDULER_ENABLED                           BT_VTPAIR( 0x84AB, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_SCHEDULER                                   BT_VTPAIR( 0x84AC, BT_VTYPE_DATA)
#define BT_EDEV_CMV_LEVEL_MANUAL                                BT_VTPAIR( 0x84AD, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_LEVEL_VACATION                              BT_VTPAIR( 0x84B4, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_LEVEL_STANDBY                               BT_VTPAIR( 0x84B5, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_LEVEL_OVERRIDE                              BT_VTPAIR( 0x84AE, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_OVERRIDE_MODE                               BT_VTPAIR( 0x84AF, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_OVERRIDE_SOURCE                             BT_VTPAIR( 0x84B0, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_OVERRIDE_UNTIL                              BT_VTPAIR( 0x84B1, BT_VTYPE_TIMESTAMP)
#define BT_EDEV_CMV_OVERRIDE                                    BT_VTPAIR( 0x84C5, BT_VTYPE_DATA)

#define BT_EDEV_CMV_BYPASS_MODE                                 BT_VTPAIR( 0x84B2, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_ALLOW_STOPPED_MODE                          BT_VTPAIR( 0x84B3, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_ALLOW_UNOCCUPIED_MODE                       BT_VTPAIR( 0x84F9, BT_VTYPE_ENUM)
#define BT_EDEV_CMV_COOLING_INTAKE_TEMP_LIMIT                   BT_VTPAIR( 0x84DA, BT_VTYPE_TEMP)

#define BT_EDEV_CMV_STATE_NAME_STOPPED                          BT_VTPAIR( 0x84D4, BT_VTYPE_TEXT)
#define BT_EDEV_CMV_STATE_NAME_UNOCCUPIED                       BT_VTPAIR( 0x84D5, BT_VTYPE_TEXT)
#define BT_EDEV_CMV_STATE_NAME_ECO                              BT_VTPAIR( 0x84D6, BT_VTYPE_TEXT)
#define BT_EDEV_CMV_STATE_NAME_COMFORT                          BT_VTPAIR( 0x84D7, BT_VTYPE_TEXT)
#define BT_EDEV_CMV_STATE_NAME_BOOST                            BT_VTPAIR( 0x84D8, BT_VTYPE_TEXT)


enum bt_edev_cmv_device_features
{
    BT_EDEV_CMV_DEVICE_FEATURES_ALLOW_UNOCCUPIED   = 0x0001,
    BT_EDEV_CMV_DEVICE_FEATURES_ALLOW_ECO          = 0x0002,
    BT_EDEV_CMV_DEVICE_FEATURES_ALLOW_COMFORT      = 0x0004,
    BT_EDEV_CMV_DEVICE_FEATURES_ALLOW_STOPPED      = 0x0008,
    BT_EDEV_CMV_DEVICE_FEATURES_ALLOW_BOOST        = 0x0010,
    BT_EDEV_CMV_DEVICE_FEATURES_ALLOW_BYPASS       = 0x0020,
    BT_EDEV_CMV_DEVICE_FEATURES_FAN_PWM_CONTROL    = 0x0040,
    BT_EDEV_CMV_DEVICE_FEATURES_FAN_BINARY_CONTROL = 0x0080,
    BT_EDEV_CMV_DEVICE_FEATURES_TEMP_INTAKE        = 0x0100,
    BT_EDEV_CMV_DEVICE_FEATURES_TEMP_SUPPLY        = 0x0200,
    BT_EDEV_CMV_DEVICE_FEATURES_TEMP_EXTRACT       = 0x0400,
    BT_EDEV_CMV_DEVICE_FEATURES_TEMP_EXHAUST       = 0x0800,
    BT_EDEV_CMV_DEVICE_FEATURES_HUMIDITY_INTAKE    = 0x1000,
    BT_EDEV_CMV_DEVICE_FEATURES_HUMIDITY_EXTRACT   = 0x2000,
};

enum bt_edev_cmv_device_identification_strategy
{
    BT_EDEV_CMV_DEVICE_IDENTIFICATION_STRATEGY_NON_STRICT = 0,
    BT_EDEV_CMV_DEVICE_IDENTIFICATION_STRATEGY_STRICT     = 1,
};

enum bt_edev_cmv_scheduler_enabled
{
    BT_EDEV_CMV_SCHEDULER_ENABLED_DISABLED,
    BT_EDEV_CMV_SCHEDULER_ENABLED_ENABLED,
    BT_EDEV_CMV_SCHEDULER_ENABLED_CREATE_SCHEDULER,
};

enum bt_edev_cmv_override_mode {
    BT_EDEV_CMV_OVERRIDE_MODE_NONE      = 0,
    BT_EDEV_CMV_OVERRIDE_MODE_TEMPORARY = 1,
    BT_EDEV_CMV_OVERRIDE_MODE_ADJUST    = 3,
};

enum bt_edev_cmv_override_source {
    BT_EDEV_CMV_OVERRIDE_SOURCE_USER = 0,
    BT_EDEV_CMV_OVERRIDE_SOURCE_HUMIDITY_CONTROL,
    BT_EDEV_CMV_OVERRIDE_SOURCE_FREE_COOLING,
    BT_EDEV_CMV_OVERRIDE_SOURCE_EXTERNAL_CONTROL,
};

enum bt_edev_cmv_override_priority {
    BT_EDEV_CMV_OVERRIDE_PRIORITY_UNDEFINED = 0,
    BT_EDEV_CMV_OVERRIDE_PRIORITY_1         = 1,  // Protection, highest priority
    BT_EDEV_CMV_OVERRIDE_PRIORITY_4         = 4,  // User override
    BT_EDEV_CMV_OVERRIDE_PRIORITY_8         = 8,  // High priority override
    BT_EDEV_CMV_OVERRIDE_PRIORITY_13        = 13, // Low priority override
    BT_EDEV_CMV_OVERRIDE_PRIORITY_15        = 15, // Regular operation
};

enum bt_edev_cmv_bypass_mode
{
    BT_EDEV_CMV_BYPASS_MODE_DISABLED = 0,
    BT_EDEV_CMV_BYPASS_MODE_ENABLED,
};

enum bt_edev_cmv_allow_stopped_mode
{
    BT_EDEV_CMV_ALLOW_STOPPED_MODE_DISABLED = 0,
    BT_EDEV_CMV_ALLOW_STOPPED_MODE_ENABLED,
};

enum bt_edev_cmv_allow_unoccupied_mode
{
    BT_EDEV_CMV_ALLOW_UNOCCUPIED_MODE_DISABLED = 0,
    BT_EDEV_CMV_ALLOW_UNOCCUPIED_MODE_ENABLED,
};

enum bt_edev_cmv_device_state
{
    BT_EDEV_CMV_DEVICE_STATE_DISCONNECTED = 0,
    BT_EDEV_CMV_DEVICE_STATE_SYNCHRONIZING,
    BT_EDEV_CMV_DEVICE_STATE_READY,
};

typedef struct bt_edev_cmv_fans_max_volume
{
    uint16_t exhaust_fan_max_volume;
    uint16_t supply_fan_max_volume;
} bt_edev_cmv_fans_max_volume;

typedef struct bt_edev_cmv_override
{
    uint32_t level    :4;  // 0 STOPPED, 1 UNOCCUPIED, 2 ECO, 3 COMFORT, 4 BOOST
    uint32_t mode     :4;  // 0 NONE, 1 TEMPORARY, 3 ADJUST
    uint32_t source   :8;  // 0 USER, 1 HUMIDITY_CONTROL, 2 FREE_COOLING
    uint32_t priority :4;  // 0 UNDEFINED, 1..15 PRIORITY (lower number, higher priority)
    uint32_t          :12; // Keep zero
    uint32_t until;        // Timestamp
} bt_edev_cmv_override;

enum bt_edev_cmv_cloud_ventilation_state
{
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_STOPPED = 0,
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_UNOCCUPIED,
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_ECO,
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_COMFORT,
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_BOOST,
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_BLOCKED,
    BT_EDEV_CMV_CLOUD_VENTILATION_STATE_FAILURE,
};

enum bt_edev_cmv_cloud_device_state
{
    BT_EDEV_CMV_CLOUD_DEVICE_STATE_DISCONNECTED = 0,
    BT_EDEV_CMV_CLOUD_DEVICE_STATE_SYNCHRONIZATION,
    BT_EDEV_CMV_CLOUD_DEVICE_STATE_READY,
};

enum bt_edev_cmv_cloud_bypass_state
{
    BT_EDEV_CMV_CLOUD_BYPASS_STATE_NO_BYPASS = 0,
    BT_EDEV_CMV_CLOUD_BYPASS_STATE_BYPASS,
};

enum bt_edev_cmv_cloud_allow_vacation_away
{
    BT_EDEV_CMV_CLOUD_ALLOW_VACATION_AWAY_DISABLED = 0,
    BT_EDEV_CMV_CLOUD_ALLOW_VACATION_AWAY_ENABLED,
};

enum bt_edev_cmv_cloud_override_level {
    BT_EDEV_CMV_CLOUD_OVERRIDE_LEVEL_STOPPED = 0,
    BT_EDEV_CMV_CLOUD_OVERRIDE_LEVEL_UNOCCUPIED,
    BT_EDEV_CMV_CLOUD_OVERRIDE_LEVEL_ECO,
    BT_EDEV_CMV_CLOUD_OVERRIDE_LEVEL_COMFORT,
    BT_EDEV_CMV_CLOUD_OVERRIDE_LEVEL_BOOST,
};

enum bt_edev_cmv_cloud_override_mode {
    BT_EDEV_CMV_CLOUD_OVERRIDE_MODE_NONE = 0,
    BT_EDEV_CMV_CLOUD_OVERRIDE_MODE_TEMPORARY,
    BT_EDEV_CMV_CLOUD_OVERRIDE_MODE_ADJUST,
};

enum bt_edev_cmv_cloud_override_source {
    BT_EDEV_CMV_CLOUD_OVERRIDE_SOURCE_NONE = 0,
    BT_EDEV_CMV_CLOUD_OVERRIDE_SOURCE_RH,
};

struct bt_edev_cmv_cloud_override
{
    uint8_t level  :4;  // 0 STOPPED, 1 UNOCCUPIED, 2 ECO, 3 COMFORT, 4 BOOST
    uint8_t mode   :4;  // 0 NONE, 1 TEMPORARY, 3 ADJUST
    uint8_t source;     // 0 NONE, 1 RH
    uint16_t reserved;  // Keep zero
    uint32_t until;     // Timestamp
};

enum bt_edev_cmv_cloud_bypass_mode {
    BT_EDEV_CMV_CLOUD_BYPASS_MODE_DISABLED = 0,
    BT_EDEV_CMV_CLOUD_BYPASS_MODE_ENABLED,
};

enum bt_edev_cmv_cloud_ack_dev_specific_err {
    BT_EDEV_CMV_CLOUD_ACK_DEV_SPECIFIC_ERR_NONE = 0,
    BT_EDEV_CMV_CLOUD_ACK_DEV_SPECIFIC_ERR_ACK_REQUIRED,
    BT_EDEV_CMV_CLOUD_ACK_DEV_SPECIFIC_ERR_ACKNOWLEDGED
};

enum bt_edev_cmv_cloud_ack_dev_specific_warn {
    BT_EDEV_CMV_CLOUD_ACK_DEV_SPECIFIC_WARN_NONE = 0,
    BT_EDEV_CMV_CLOUD_ACK_DEV_SPECIFIC_WARN_ACK_REQUIRED,
    BT_EDEV_CMV_CLOUD_ACK_DEV_SPECIFIC_WARN_ACKNOWLEDGED
};

//-------------------------------------------------------------------------------------------------------------------------

/**
 * @defgroup output Output
 * @{
 */

/**
 * @defgroup analog_output Analog output
 */

/**
 * @defgroup output_valvehead Valvehead (SRT) output
 */

/**
 * @defgroup output_thermohead Thermohead output
 */

#define BT_OUTPUT_VALUE_SOURCE                                  BT_VTPAIR( 0x80A0, BT_VTYPE_DATA)
#define BT_OUTPUT_BLOCK_SOURCE                                  BT_VTPAIR( 0x80A9, BT_VTYPE_DATA)
#define BT_OUTPUT_VALUE_THRESHOLD                               BT_VTPAIR( 0x80A3, BT_VTYPE_D2_FP100)   // universal temp/percent
#define BT_OUTPUT_BLOCK_THRESHOLD                               BT_VTPAIR( 0x80F1, BT_VTYPE_D2_FP100)
#define BT_OUTPUT_SOURCE_MIN_VALUE                              BT_VTPAIR( 0x80A1, BT_VTYPE_D2_FP100)
#define BT_OUTPUT_SOURCE_MAX_VALUE                              BT_VTPAIR( 0x80A2, BT_VTYPE_D2_FP100)
#define BT_OUTPUT_SERVICE_MODE                                  BT_VTPAIR( 0x80A5, BT_VTYPE_ENUM)
#define BT_OUTPUT_SERVICE_MODE_END_TIME                         BT_VTPAIR( 0x8129, BT_VTYPE_TIMESTAMP)
#define BT_OUTPUT_SERVICE_VALUE                                 BT_VTPAIR( 0x80A6, BT_VTYPE_D2_FP100)
#define BT_OUTPUT_DELAY_START                                   BT_VTPAIR( 0x80A7, BT_VTYPE_U2)
#define BT_OUTPUT_DELAY_END                                     BT_VTPAIR( 0x80A8, BT_VTYPE_U2)
#define BT_OUTPUT_INVERTED                                      BT_VTPAIR( 0x80AA, BT_VTYPE_ENUM)
#define BT_OUTPUT_OUTPUT_VALUE                                  BT_VTPAIR( 0x4C  , BT_VTYPE_PERCENT)
#define BT_OUTPUT_FUNCTION                                      BT_VTPAIR( 0x80E7, BT_VTYPE_ENUM)
#define BT_OUTPUT_SERVO_TYPE                                    BT_VTPAIR( 0x80E9, BT_VTYPE_ENUM)
#define BT_OUTPUT_SERVO_RUNTIME                                 BT_VTPAIR( 0x80EA, BT_VTYPE_U2)
#define BT_OUTPUT_SERVO_WINDUP                                  BT_VTPAIR( 0x80EB, BT_VTYPE_D2_FP10)
#define BT_OUTPUT_SERVO_REBOUND                                 BT_VTPAIR( 0x80EC, BT_VTYPE_D2_FP10)
#define BT_OUTPUT_SERVO_DEADTIME                                BT_VTPAIR( 0x80ED, BT_VTYPE_U2)
#define BT_OUTPUT_ALARM_OUTPUT_FAIL                             BT_VTPAIR( 0x4015, BT_VTYPE_WARNING)
#define BT_OUTPUT_ERR_INVALID_REFERENCE                         BT_VTPAIR( 0x4045, BT_VTYPE_WARNING)
#define BT_OUTPUT_MANUAL_VALUE                                  BT_VTPAIR( 0x80F0, BT_VTYPE_D2_FP100)
#define BT_OUTPUT_LAST_ACTIVATION_NON_PERSISTENT                BT_VTPAIR( 0x5C  , BT_VTYPE_U4)
#define BT_OUTPUT_LAST_ACTIVATION                               BT_VTPAIR( 0x8485, BT_VTYPE_U4)
#define BT_OUTPUT_EXERCISE_CYCLE_LENGTH                         BT_VTPAIR( 0x8112, BT_VTYPE_U2)
#define BT_OUTPUT_EXERCISE_ENABLED                              BT_VTPAIR( 0x8111, BT_VTYPE_U1)
#define BT_OUTPUT_EXERCISE_IDLE_TIME                            BT_VTPAIR( 0x8110, BT_VTYPE_U4)
#define BT_OUTPUT_EXERCISE_STATUS                               BT_VTPAIR( 0x5D  , BT_VTYPE_ENUM)
#define BT_OUTPUT_EXERCISE_BLOCKED                              BT_VTPAIR( 0x7D  , BT_VTYPE_U1)
#define BT_OUTPUT_INDICATION_OVERRIDE                           BT_VTPAIR( 0xBC  , BT_VTYPE_DATA)


enum bt_output_indication_override_color {
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_BLACK       = 0,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_BLUE        = 1,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_GREEN       = 2,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_CYAN        = 3,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_RED         = 4,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_MAGENTA     = 5,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_YELLOW      = 6,
    BT_OUTPUT_INDICATION_OVERRIDE_COLOR_WHITE       = 7,
};

typedef struct PACK_BT_DATA bt_output_indication_override {
    uint16_t color_idle             :4;
    uint16_t color_active           :4;
    uint16_t color_blocked_active   :4;
    uint16_t color_blocked_idle     :4;
    uint8_t blocked                 :1;
    uint8_t alarm                   :1;
    uint8_t error                   :1;
    uint8_t                         :5;
    uint8_t reserved[1];
} bt_output_indication_override;


/**
 * @addtogroup output_analog
 * @{
 */
#define BT_OUTPUT_ANALOG_MAX_VALUE_VOLTAGE                      BT_VTPAIR( 0x80F7, BT_VTYPE_VOLT)
#define BT_OUTPUT_ANALOG_MIN_VALUE_VOLTAGE                      BT_VTPAIR( 0x80F8, BT_VTYPE_VOLT)
#define BT_OUTPUT_ANALOG_NO_DEMAND_VOLTAGE                      BT_VTPAIR( 0x810F, BT_VTYPE_VOLT)
/**
 * @}
 */

/**
 * @addtogroup output_valvehead
 * @{
 */
#define BT_OUTPUT_VALVEHEAD_DEMAND                              BT_VTPAIR( 0x6A  , BT_VTYPE_PERCENT)
#define BT_OUTPUT_VALVEHEAD_DEMAND_THRESHOLD                    BT_VTPAIR( 0x8465, BT_VTYPE_PERCENT)
//#define BT_OUTPUT_VALVEHEAD_DISCOVERED_WORKING_SPAN			BT_VTPAIR( 0x105 , BT_VTYPE_D2_FP100)
#define BT_OUTPUT_VALVEHEAD_FC_FO_DISCOVERED					BT_VTPAIR( 0x108 , BT_VTYPE_DATA)
#define BT_OUTPUT_VALVEHEAD_WORKING_SPAN_PRESET					BT_VTPAIR( 0x84DD, BT_VTYPE_D2_FP100)

struct bt_output_valvehead_discovered_working_span
{
    uint16_t begin;
    uint16_t end;
};

/**
 * @}
 */

/**
 * @addtogroup output_thermohead
 * @{
 */
#define BT_OUTPUT_THERMOHEAD_WARN_NO_LOAD_DETECTED              BT_VTPAIR( 0x4070, BT_VTYPE_WARNING)
#define BT_OUTPUT_THERMOHEAD_LOAD_DETECTED                      BT_VTPAIR( 0xB0  , BT_VTYPE_U1)
#define BT_OUTPUT_THERMOHEAD_LOAD_POWER                         BT_VTPAIR( 0xBE  , BT_VTYPE_U2_FP10)
#define BT_OUTPUT_THERMOHEAD_LOAD_TYPE                          BT_VTPAIR( 0x847C, BT_VTYPE_ENUM)
#define BT_OUTPUT_THERMOHEAD_FIRST_OPEN_PERFORMED               BT_VTPAIR( 0x8487, BT_VTYPE_ENUM)
/**
 * @}
 */

/**
 * @deprecated Use enum bt_output_exercise_status
 * @addtogroup Names are deprecated
 * @{
 */
#define BT_OUTPUT_PERIODIC_ACT_REQUEST                          BT_VTPAIR( 0x5D  , BT_VTYPE_U1)
#define BT_OUTPUT_PERIODIC_ACT_IDLE_TIME                        BT_VTPAIR( 0x8110, BT_VTYPE_U4)
#define BT_OUTPUT_PERIODIC_ACT_CYCLES                           BT_VTPAIR( 0x8111, BT_VTYPE_U1)
#define BT_OUTPUT_PERIODIC_ACT_CYCLE_LENGTH                     BT_VTPAIR( 0x8112, BT_VTYPE_U2)
/**
 * @}
 */

#define BT_GPIO_MODE                                            BT_VTPAIR( 0x80FD, BT_VTYPE_ENUM)

enum bt_output_servo_type
{
    BT_OUTPUT_SERVO_TYPE_NOT_CONNECTED,
    BT_OUTPUT_SERVO_TYPE_ANALOG_0_10V,
    BT_OUTPUT_SERVO_TYPE_3POINT,
    BT_OUTPUT_SERVO_TYPE_ANALOG_10_0V,
};

enum bt_output_relay_value {
    BT_OUTPUT_RELAY_VALUE_OFF         = 0,
    BT_OUTPUT_RELAY_VALUE_OFF_OVERRIDE,       // output blocked by magnet
    BT_OUTPUT_RELAY_VALUE_OFF_WAITING,        // delayed start
    BT_OUTPUT_RELAY_VALUE_ON,
    BT_OUTPUT_RELAY_VALUE_ON_OVERRIDE,        // anti-jam cycle
    BT_OUTPUT_RELAY_VALUE_ON_WAITING,         // delayed end
};

enum bt_output_function {
    BT_OUTPUT_FUNCTION_OFF                   = 0,
    BT_OUTPUT_FUNCTION_MANUAL,
    BT_OUTPUT_FUNCTION_MAX_VALUE,
    BT_OUTPUT_FUNCTION_MIN_VALUE,
    BT_OUTPUT_FUNCTION_THERMOHEAD,
    BT_OUTPUT_FUNCTION_HEAT_DEMAND,
    BT_OUTPUT_FUNCTION_SERVO,
    BT_OUTPUT_FUNCTION_ANALOG_HC_CHANGE_OVER,
    BT_OUTPUT_FUNCTION_ANALOG_PROPORTIONAL_THRESHOLD,
    BT_OUTPUT_FUNCTION_THERMOHEAD_RADIATOR,
    BT_OUTPUT_FUNCTION_VALVEHEAD_RADIATOR_AUTONOMOUS,
    BT_OUTPUT_FUNCTION_VALVEHEAD_RADIATOR,
    BT_OUTPUT_FUNCTION_VALVEHEAD_FLOOR,

    BT_OUTPUT_FUNCTION_THERMOHEAD_FLOOR = BT_OUTPUT_FUNCTION_THERMOHEAD,

};

//enum bt_output_actuator {
//    BT_OUTPUT_ACTUATOR_RELAY                 = 0,
//    BT_OUTPUT_ACTUATOR_ANALOG,
//  BT_OUTPUT_ACTUATOR_SERVO
//};

enum bt_output_service_mode {
    BT_OUTPUT_SERVICE_MODE_OFF              = 0,
    BT_OUTPUT_SERVICE_MODE_ON,
};

enum bt_output_inverterd {
    BT_OUTPUT_INVERTED_OFF                  = 0,
    BT_OUTPUT_INVERTED_ON,
};

enum bt_gpio_mode {
    BT_GPIO_MODE_INPUT,
    BT_GPIO_MODE_OUTPUT_NO_PULL,
    BT_GPIO_MODE_OUTPUT_PULL_UP,
};

enum bt_output_exercise_status {
    BT_OUTPUT_EXERCISE_STATUS_IDLE = 0,
    BT_OUTPUT_EXERCISE_STATUS_PENDING,
    BT_OUTPUT_EXERCISE_STATUS_REQUIRED,
    BT_OUTPUT_EXERCISE_STATUS_EXERCISING,

    // Meaning of BT_OUTPUT_EXERCISE_STATUS_REQUIRED has changed, now it means
    // that the output was never activated before and needs FOA to be performed.
    BT_OUTPUT_EXERCISE_STATUS_NEVER_EXERCISED = BT_OUTPUT_EXERCISE_STATUS_REQUIRED,
};

enum bt_output_thermohead_load_type {
    BT_OUTPUT_THERMOHEAD_LOAD_TYPE_THERMOHEAD   = 0,
    BT_OUTPUT_THERMOHEAD_LOAD_TYPE_RELAY,
};

typedef enum
{
    BT_GPIO_SUBTYPE_PROFILE_GPIO,

    BT_GPIO_SUBTYPE_GPIO = BT_GPIO_SUBTYPE_PROFILE_GPIO | (1 << 7),
} bt_gpio_subtype_t;

/**
 * @}
 */

//-------------------------------------------------------------------------------------------------------------------------

#define BT_UPDATE_CTRL_MODE								BT_VTPAIR( 0x812A, BT_VTYPE_ENUM)
#define BT_UPDATE_CTRL_STATE							BT_VTPAIR( 0x812B, BT_VTYPE_ENUM)
#define BT_UPDATE_CTRL_ONLINE_DEVICES					BT_VTPAIR( 0x70  , BT_VTYPE_U1)
#define BT_UPDATE_CTRL_OFFLINE_DEVICES					BT_VTPAIR( 0x71  , BT_VTYPE_U1)
#define BT_UPDATE_CTRL_STORED_FW_PACKAGE_NAME			BT_VTPAIR( 0x812E, BT_VTYPE_TEXT)
#define BT_UPDATE_CTRL_INSTALLED_FW_PACKAGE_VERSION		BT_VTPAIR( 0x8133, BT_VTYPE_U2)
#define BT_UPDATE_CTRL_DEVICES_TO_UPDATE				BT_VTPAIR( 0x812F, BT_VTYPE_U1)
#define BT_UPDATE_CTRL_UPDATE_ALL_TIME					BT_VTPAIR( 0x8130, BT_VTYPE_U2)
#define BT_UPDATE_CTRL_UPDATE_CCU_TIME					BT_VTPAIR( 0x8131, BT_VTYPE_U2)
#define BT_UPDATE_CTRL_UPDATE_CCU_TIMEOUT				BT_VTPAIR( 0x8132, BT_VTYPE_TIMESTAMP)
#define BT_UPDATE_CTRL_PROGRESS_DEVICE_IDX				BT_VTPAIR( 0x6D  , BT_VTYPE_U1)
#define BT_UPDATE_CTRL_PROGRESS_DEVICE_PERCENT			BT_VTPAIR( 0x6E  , BT_VTYPE_U1)
#define BT_UPDATE_CTRL_EMUL_END_STATE					BT_VTPAIR( 0x812C, BT_VTYPE_ENUM)
#define BT_UPDATE_CTRL_EMUL_ONLINE_DEVICES				BT_VTPAIR( 0x812D, BT_VTYPE_U1)
#define BT_UPDATE_CTRL_EMUL_OFFLINE_DEVICES				BT_VTPAIR( 0x8136, BT_VTYPE_U1)
#define BT_UPDATE_CTRL_EMUL_FORCE_CCU_UPDATE			BT_VTPAIR( 0x8137, BT_VTYPE_U1)
#define BT_UPDATE_CTRL_REPORT_STATE_TIME				BT_VTPAIR( 0x813A, BT_VTYPE_TIMESTAMP)
#define BT_UPDATE_CTRL_NEXT_UPDATE_CHECK				BT_VTPAIR( 0x813C, BT_VTYPE_TIMESTAMP)
#define BT_UPDATE_CTRL_WARN_CRITICAL_UPDATE_AVAILABLE	BT_VTPAIR( 0x402C, BT_VTYPE_U1)

enum bt_update_ctrl_state {
    BT_UPDATE_CTRL_STATE_IDLE					= 0,
    BT_UPDATE_CTRL_STATE_CHECKING				= 1,
    BT_UPDATE_CTRL_STATE_CHECKING_FAIL			= 2,
    BT_UPDATE_CTRL_STATE_UPDATE_NOT_AVAILABLE	= 3,
    BT_UPDATE_CTRL_STATE_UPDATE_AVAILABLE		= 4,
    BT_UPDATE_CTRL_STATE_UPDATING_CCU			= 5,
    BT_UPDATE_CTRL_STATE_UPDATING_PERIPHERAL	= 6,
    BT_UPDATE_CTRL_STATE_UPDATE_REJECTED		= 7,
    BT_UPDATE_CTRL_STATE_UPDATE_FAILED			= 8,
    BT_UPDATE_CTRL_STATE_UPDATE_FINISHED		= 9,
};

enum bt_update_ctrl_mode {
    // Illogical order is because of back compatibility with Sentio Update UI Demo application
    BT_UPDATE_CTRL_MODE_DISABLED_MOBILE_APP		= 0,
    BT_UPDATE_CTRL_MODE_ENABLED					= 1,
    BT_UPDATE_CTRL_MODE_DISABLED_ENTIRELY		= 2,
};

//-------------------------------------------------------------------------------------------------------------------------

#define BT_DEBUG_STORAGE_BUFFER_OVERFLOW						BT_VTPAIR( 0xEFFF, BT_VTYPE_TEXT)
#define BT_DEBUG_MINIMUM_EVER_FREE_HEAP_SIZE					BT_VTPAIR( 0xE051, BT_VTYPE_U4)

// VH-250 controllers
#define BT_DEBUG_INTERNAL_EXERCISE_STATUS						BT_VTPAIR( 0xE000, BT_VTYPE_U1)
#define BT_DEBUG_VALVE_STATUS									BT_VTPAIR( 0xE001, BT_VTYPE_U1)
#define BT_DEBUG_VALVE_STATE_STATUS								BT_VTPAIR( 0xE036, BT_VTYPE_ENUM)
#define BT_DEBUG_MOTOR_CONTROLLER_STATE							BT_VTPAIR( 0xE03C, BT_VTYPE_ENUM)
#define BT_DEBUG_MOTOR_CONTROLLER_RESULT						BT_VTPAIR( 0xE03D, BT_VTYPE_ENUM)
#define BT_DEBUG_COOLING_CONTROLLER_STATUS						BT_VTPAIR( 0xE03F, BT_VTYPE_ENUM)
#define BT_DEBUG_FROST_PROTECTION_STATUS						BT_VTPAIR( 0xE040, BT_VTYPE_ENUM)
#define BT_DEBUG_CONNECTION_LOST_BEHAVIOR						BT_VTPAIR( 0xE041, BT_VTYPE_ENUM)
#define BT_DEBUG_PERIODIC_ACTIVATION_SCHEDULER_STATE			BT_VTPAIR( 0xE050, BT_VTYPE_ENUM)
#define BT_DEBUG_PERIODIC_ACTIVATION_PATTERN_FINDER_STATE		BT_VTPAIR( 0xE052, BT_VTYPE_ENUM)
#define BT_DEBUG_EMPTY_BATTERY_BEHAVIOR_STATE					BT_VTPAIR( 0xE054, BT_VTYPE_ENUM)
#define BT_DEBUG_BATTERY_STATE									BT_VTPAIR( 0xE055, BT_VTYPE_ENUM)
#define BT_DEBUG_MOTOR_CAL_FC_MM								BT_VTPAIR( 0xE056, BT_VTYPE_U2_FP100)
#define BT_DEBUG_MOTOR_CAL_FO_MM								BT_VTPAIR( 0xE057, BT_VTYPE_U2_FP100)

// ROXi stats diagnostics
#define BT_DEBUG_DATAGRAMS_SENT									BT_VTPAIR( 0xE002, BT_VTYPE_U4)
#define BT_DEBUG_DATAGRAMS_RECEIVED								BT_VTPAIR( 0xE003, BT_VTYPE_U4)
#define BT_DEBUG_BYTES_SENT 									BT_VTPAIR( 0xE004, BT_VTYPE_U4)
#define BT_DEBUG_BYTES_RECEIVED									BT_VTPAIR( 0xE005, BT_VTYPE_U4)
#define BT_DEBUG_VALUES_SENT					 				BT_VTPAIR( 0xE006, BT_VTYPE_U4)
#define BT_DEBUG_VALUES_RECEIVED								BT_VTPAIR( 0xE007, BT_VTYPE_U4)
#define BT_DEBUG_RX_FAILS										BT_VTPAIR( 0xE008, BT_VTYPE_U4)
#define BT_DEBUG_LBT_OK											BT_VTPAIR( 0xE009, BT_VTYPE_U4)
#define BT_DEBUG_LBT_FAIL										BT_VTPAIR( 0xE00A, BT_VTYPE_U4)
#define BT_DEBUG_RSSI_RECEIVED_BY_PERIPHERAL					BT_VTPAIR( 0xE00B, BT_VTYPE_D1)
#define BT_DEBUG_RSSI_RECEIVED_BY_CCU							BT_VTPAIR( 0xE00C, BT_VTYPE_D1)
#define BT_DEBUG_CONNECTION_QUALITY								BT_VTPAIR( 0xE00D, BT_VTYPE_PERCENT)
#define BT_DEBUG_RADIO_POWER_CONSUMTION							BT_VTPAIR( 0xE00E, BT_VTYPE_U4)
#define BT_DEBUG_RADIO_RESTART									BT_VTPAIR( 0xE00F, BT_VTYPE_U4)
#define BT_DEBUG_RADIO_FAILS									BT_VTPAIR( 0xE010, BT_VTYPE_U4)

// PID regulator diagnostics
#define BT_DEBUG_PID_REGULATOR_P_VALUE							BT_VTPAIR( 0xE013, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_I_VALUE							BT_VTPAIR( 0xE014, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_I_VALUE_IN_TIME		  			BT_VTPAIR( 0xE03E, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_D_VALUE							BT_VTPAIR( 0xE015, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_E_VALUE							BT_VTPAIR( 0xE016, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_E_VALUE_FILTERED					BT_VTPAIR( 0xE037, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_MANIPULATED_VALUE				BT_VTPAIR( 0xE017, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_KP								BT_VTPAIR( 0xE018, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_KI								BT_VTPAIR( 0xE019, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_KD								BT_VTPAIR( 0xE01A, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_SETPOINT							BT_VTPAIR( 0xE02D, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_MEASURED							BT_VTPAIR( 0xE02E, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_ACTION							BT_VTPAIR( 0xE02F, BT_VTYPE_U4)
#define BT_DEBUG_PID_REGULATOR_AVS								BT_VTPAIR( 0xE033, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_SP_CHANGE_EVENT					BT_VTPAIR( 0xE03B, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_OUTPUT_VALUE						BT_VTPAIR( 0xE034, BT_VTYPE_D4)
#define BT_DEBUG_PID_REGULATOR_SETPOINT_ERROR_IN_TIME			BT_VTPAIR( 0xE038, BT_VTYPE_D4)

// Temporary VH-250 regulator constnts for tests
#define BT_VH250_REG_KP_SET										BT_VTPAIR( 0x8442, BT_VTYPE_PERCENT)
#define BT_VH250_REG_KI_SET										BT_VTPAIR( 0x8443, BT_VTYPE_PERCENT)
#define BT_VH250_REG_KD_SET										BT_VTPAIR( 0x8444, BT_VTYPE_PERCENT)
#define BT_VH250_REG_AVS_SET									BT_VTPAIR( 0x8479, BT_VTYPE_PERCENT)
#define BT_VH250_REG_IRA_SET									BT_VTPAIR( 0x8484, BT_VTYPE_TEMP)

// Dryer VID's for RS-211 room curve emulator (project target TL683 in TL603 git space)
// These values is used for emulator settings
//-------------------------------------------------------------------------------------------------------------------------
#define BT_DRYER_SET_TEMP_PHASE1_LEN							BT_VTPAIR( 0x8457, BT_VTYPE_D4)
#define BT_DRYER_SET_TEMP_PHASE2_LEN							BT_VTPAIR( 0x8458, BT_VTYPE_D4)
#define BT_DRYER_SET_HUMI_PHASE1_LEN							BT_VTPAIR( 0x8459, BT_VTYPE_D4)
#define BT_DRYER_SET_HUMI_PHASE2_LEN							BT_VTPAIR( 0x845A, BT_VTYPE_D4)
#define BT_DRYER_SET_TEMP_PHASE1_VAL							BT_VTPAIR( 0x845B, BT_VTYPE_TEMP)
#define BT_DRYER_SET_TEMP_PHASE2_VAL							BT_VTPAIR( 0x845C, BT_VTYPE_TEMP)
#define BT_DRYER_SET_HUMI_PHASE1_VAL							BT_VTPAIR( 0x845D, BT_VTYPE_HUM)
#define BT_DRYER_SET_HUMI_PHASE2_VAL							BT_VTPAIR( 0x845E, BT_VTYPE_HUM)
#define BT_DRYER_SET_IDLE_TIME									BT_VTPAIR( 0x845F, BT_VTYPE_D4)



// Temperature sensors diagnostics
#define BT_DEBUG_AIR_TEMPERATURE_RAW							BT_VTPAIR( 0xE01B, BT_VTYPE_TEMP)
#define BT_DEBUG_AIR_HUMIDITY_RAW								BT_VTPAIR( 0xE01C, BT_VTYPE_HUM)
#define BT_DEBUG_BASE_TEMPERATURE_RAW							BT_VTPAIR( 0xE01D, BT_VTYPE_TEMP)
#define BT_DEBUG_TEMPERATURE_DELTA_BASE_AIR_RAW					BT_VTPAIR( 0xE02C, BT_VTYPE_TEMP)

// Debug storage diagnostics
#define BT_DEBUG_STORAGE_NOT_READY								BT_VTPAIR( 0xE01E, BT_VTYPE_U4)

// Battery management diagnostics
#define BT_DEBUG_CONSUMPTION_UI									BT_VTPAIR( 0xE01F, BT_VTYPE_PERCENT)
#define BT_DEBUG_CONSUMPTION_MOTOR								BT_VTPAIR( 0xE020, BT_VTYPE_PERCENT)
#define BT_DEBUG_CONSUMPTION_RADIO								BT_VTPAIR( 0xE021, BT_VTYPE_PERCENT)
#define BT_DEBUG_BATTERY_VOLTAGE_LOW_CURRENT					BT_VTPAIR( 0xE022, BT_VTYPE_U2)
#define BT_DEBUG_BATTERY_VOLTAGE_HIGH_CURRENT					BT_VTPAIR( 0xE023, BT_VTYPE_U2)
#define BT_DEBUG_BATTERY_VOLTAGE_LOW_CURRENT_RAW				BT_VTPAIR( 0xE058, BT_VTYPE_U2)
#define BT_DEBUG_BATTERY_VOLTAGE_HIGH_CURRENT_RAW				BT_VTPAIR( 0xE059, BT_VTYPE_U2)
#define BT_DEBUG_VBTAT_HI_CURR_RAW_NOT_REP						BT_VTPAIR( 0xE05A, BT_VTYPE_U2)
#define BT_DEBUG_VBAT_LOW_CUR_RAW_TRIG_HI_CURR_NOT_REP			BT_VTPAIR( 0xE05B, BT_VTYPE_U2)
#define BT_DEBUG_BATTERY_ESR_COMPUTED							BT_VTPAIR( 0xE024, BT_VTYPE_U2)

// Motor debug diagnostics
#define BT_DEBUG_MOTOR_STEPS_INCREMENT_OPEN						BT_VTPAIR( 0xE025, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_STEPS_INCREMENT_CLOSE					BT_VTPAIR( 0xE026, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_STEPS_TOTAL_OPEN							BT_VTPAIR( 0xE027, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_STEPS_TOTAL_CLOSE						BT_VTPAIR( 0xE028, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_STEPS_ABSOLUTE_POSITION					BT_VTPAIR( 0xE029, BT_VTYPE_D4)
#define BT_DEBUG_MOTOR_STEPS_INSTALL_STALL_FC_DIFF				BT_VTPAIR( 0xE060, BT_VTYPE_D2)

// Do not use that values in VH-250 (obsolette, aggregated into total steps below, VID: 0xE042)
// #define BT_DEBUG_MOTOR_STEPS_OPEN								BT_VTPAIR( 0xE02A, BT_VTYPE_U4)
// #define BT_DEBUG_MOTOR_STEPS_CLOSE								BT_VTPAIR( 0xE02B, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_STEPS_TOTAL								BT_VTPAIR( 0xE042, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_CAL_STEPS_CLOSED							BT_VTPAIR( 0xE030, BT_VTYPE_D2)
#define BT_DEBUG_MOTOR_CAL_STEPS_PRELOAD						BT_VTPAIR( 0xE031, BT_VTYPE_D2)
#define BT_DEBUG_MOTOR_STEPS_PER_DAY							BT_VTPAIR( 0xE011, BT_VTYPE_U4)
#define BT_DEBUG_MOTOR_STEPS_INTRADAY_TREND						BT_VTPAIR( 0xE012, BT_VTYPE_U4)


// Dev status / roxi status
#define BT_DEBUG_CLIENT_ROXI_STATUS								BT_VTPAIR( 0xE035, BT_VTYPE_U1)
#define BT_DEBUG_RESET_SOURCE									BT_VTPAIR( 0xE032, BT_VTYPE_U4)



// Dehumidifier debug values
#define BT_DEBUG_DRYING_SOURCE_DEMAND                           BT_VTPAIR( 0xE039, BT_VTYPE_U1)
#define BT_DEBUG_INTEGRATION_SOURCE_DEMAND                      BT_VTPAIR( 0xE03A, BT_VTYPE_U1)

// Adaptive mode debug
#define BT_DEBUG_ADAPTIVE_MODE_HEAT_DELAY						BT_VTPAIR( 0xE043, BT_VTYPE_U2)
#define BT_DEBUG_ADAPTIVE_MODE_GRADIENT							BT_VTPAIR( 0xE044, BT_VTYPE_U2)

// HCW debug values
#define BT_DEBUG_HCW_SRC_DEMAND_PRIMARY                         BT_VTPAIR( 0xE045, BT_VTYPE_U1)
#define BT_DEBUG_HCW_SRC_DEMAND_REQUESTED_TEMP                  BT_VTPAIR( 0xE046, BT_VTYPE_D2_FP100)
#define BT_DEBUG_HCW_SRC_STATUS_ACTIVITY                        BT_VTPAIR( 0xE047, BT_VTYPE_U1)

#define BT_DEBUG_HCW_AIR_SRC_DEMAND_PRIMARY                     BT_VTPAIR( 0xE04C, BT_VTYPE_U1)
#define BT_DEBUG_HCW_AIR_SRC_DEMAND_REQUESTED_TEMP              BT_VTPAIR( 0xE04D, BT_VTYPE_D2_FP100)
#define BT_DEBUG_HCW_UFHC_SRC_DEMAND_PRIMARY                    BT_VTPAIR( 0xE04E, BT_VTYPE_U1)
#define BT_DEBUG_HCW_UFHC_SRC_DEMAND_REQUESTED_TEMP             BT_VTPAIR( 0xE04F, BT_VTYPE_D2_FP100)

// Periodic activation debug values
#define BT_DEBUG_LOCATION_EXERCISING_STATUS                     BT_VTPAIR( 0xE048, BT_VTYPE_ENUM)

enum bt_debug_location_exercising_status {
    BT_DEBUG_LOCATION_EXERCISING_STATUS_IDLE                    = 0,
    BT_DEBUG_LOCATION_EXERCISING_STATUS_CHECKING                = 1,
    BT_DEBUG_LOCATION_EXERCISING_STATUS_EXERCISING_ACTUATORS    = 2,
    BT_DEBUG_LOCATION_EXERCISING_STATUS_EXERCISING_PUMPS        = 3,
    BT_DEBUG_LOCATION_EXERCISING_STATUS_EXERCISING_SERVOS       = 4,
};

// ITC controller debug values
#define BT_DEBUG_ITC_RAMPING_MODIFIER                           BT_VTPAIR( 0xE049, BT_VTYPE_TEMP)
#define BT_DEBUG_ITC_BOOST_MODIFIER                             BT_VTPAIR( 0xE04A, BT_VTYPE_TEMP)
#define BT_DEBUG_ITC_RETURN_LIMITER_MODIFIER                    BT_VTPAIR( 0xE04B, BT_VTYPE_TEMP)


// Broker debug values
#define BT_DEBUG_BROKER_FLASH_REWRITE_COUNTER                   BT_VTPAIR( 0xE053, BT_VTYPE_U4)


//-------------------------------------------------------------------------------------------------------------------------
//Testing
//Alocated for testing purposes only
//Mustn't be used in any production device!

#define BT_TEST_M00                                             BT_VTPAIR( 0xC5,   BT_VTYPE_U1)
#define BT_TEST_M01                                             BT_VTPAIR( 0xC6,   BT_VTYPE_U1)
#define BT_TEST_M02                                             BT_VTPAIR( 0xC7,   BT_VTYPE_U2)
#define BT_TEST_M03                                             BT_VTPAIR( 0xC8,   BT_VTYPE_U2)
#define BT_TEST_M04                                             BT_VTPAIR( 0xC9,   BT_VTYPE_U4)
#define BT_TEST_M05                                             BT_VTPAIR( 0xCA,   BT_VTYPE_U4)
#define BT_TEST_M06                                             BT_VTPAIR( 0xCB,   BT_VTYPE_D1)
#define BT_TEST_M07                                             BT_VTPAIR( 0xCC,   BT_VTYPE_D1)
#define BT_TEST_M08                                             BT_VTPAIR( 0xCD,   BT_VTYPE_D2)
#define BT_TEST_M09                                             BT_VTPAIR( 0xCE,   BT_VTYPE_D2)
#define BT_TEST_M10                                             BT_VTPAIR( 0xCF,   BT_VTYPE_D4)
#define BT_TEST_M11                                             BT_VTPAIR( 0xD0,   BT_VTYPE_D4)
#define BT_TEST_M12                                             BT_VTPAIR( 0xD1,   BT_VTYPE_U2_FP10)
#define BT_TEST_M13                                             BT_VTPAIR( 0xD2,   BT_VTYPE_U2_FP10)
#define BT_TEST_M14                                             BT_VTPAIR( 0xD3,   BT_VTYPE_U2_FP100)
#define BT_TEST_M15                                             BT_VTPAIR( 0xD4,   BT_VTYPE_U2_FP100)
#define BT_TEST_M16                                             BT_VTPAIR( 0xD5,   BT_VTYPE_D2_FP10)
#define BT_TEST_M17                                             BT_VTPAIR( 0xD6,   BT_VTYPE_D2_FP10)
#define BT_TEST_M18                                             BT_VTPAIR( 0xD7,   BT_VTYPE_D2_FP100)
#define BT_TEST_M19                                             BT_VTPAIR( 0xD8,   BT_VTYPE_D2_FP100)
#define BT_TEST_M20                                             BT_VTPAIR( 0xD9,   BT_VTYPE_TEXT)
#define BT_TEST_M21                                             BT_VTPAIR( 0xDA,   BT_VTYPE_TEXT)
#define BT_TEST_M22                                             BT_VTPAIR( 0xDB,   BT_VTYPE_DATA)
#define BT_TEST_M23                                             BT_VTPAIR( 0xDC,   BT_VTYPE_DATA)

#define BT_TEST_A00                                             BT_VTPAIR( 0x4054, BT_VTYPE_U1)
#define BT_TEST_A01                                             BT_VTPAIR( 0x4055, BT_VTYPE_U1)
#define BT_TEST_A02                                             BT_VTPAIR( 0x4056, BT_VTYPE_U2)
#define BT_TEST_A03                                             BT_VTPAIR( 0x4057, BT_VTYPE_U2)
#define BT_TEST_A04                                             BT_VTPAIR( 0x4058, BT_VTYPE_U4)
#define BT_TEST_A05                                             BT_VTPAIR( 0x4059, BT_VTYPE_U4)
#define BT_TEST_A06                                             BT_VTPAIR( 0x405A, BT_VTYPE_D1)
#define BT_TEST_A07                                             BT_VTPAIR( 0x405B, BT_VTYPE_D1)
#define BT_TEST_A08                                             BT_VTPAIR( 0x405C, BT_VTYPE_D2)
#define BT_TEST_A09                                             BT_VTPAIR( 0x405D, BT_VTYPE_D2)
#define BT_TEST_A10                                             BT_VTPAIR( 0x405E, BT_VTYPE_D4)
#define BT_TEST_A11                                             BT_VTPAIR( 0x405F, BT_VTYPE_D4)
#define BT_TEST_A12                                             BT_VTPAIR( 0x4060, BT_VTYPE_U2_FP10)
#define BT_TEST_A13                                             BT_VTPAIR( 0x4061, BT_VTYPE_U2_FP10)
#define BT_TEST_A14                                             BT_VTPAIR( 0x4062, BT_VTYPE_U2_FP100)
#define BT_TEST_A15                                             BT_VTPAIR( 0x4063, BT_VTYPE_U2_FP100)
#define BT_TEST_A16                                             BT_VTPAIR( 0x4064, BT_VTYPE_D2_FP10)
#define BT_TEST_A17                                             BT_VTPAIR( 0x4065, BT_VTYPE_D2_FP10)
#define BT_TEST_A18                                             BT_VTPAIR( 0x4066, BT_VTYPE_D2_FP100)
#define BT_TEST_A19                                             BT_VTPAIR( 0x4067, BT_VTYPE_D2_FP100)
#define BT_TEST_A20                                             BT_VTPAIR( 0x4068, BT_VTYPE_TEXT)
#define BT_TEST_A21                                             BT_VTPAIR( 0x4069, BT_VTYPE_TEXT)
#define BT_TEST_A22                                             BT_VTPAIR( 0x406A, BT_VTYPE_DATA)
#define BT_TEST_A23                                             BT_VTPAIR( 0x406B, BT_VTYPE_DATA)

#define BT_TEST_P00                                             BT_VTPAIR( 0x848E, BT_VTYPE_U1)
#define BT_TEST_P01                                             BT_VTPAIR( 0x848F, BT_VTYPE_U1)
#define BT_TEST_P02                                             BT_VTPAIR( 0x8490, BT_VTYPE_U2)
#define BT_TEST_P03                                             BT_VTPAIR( 0x8491, BT_VTYPE_U2)
#define BT_TEST_P04                                             BT_VTPAIR( 0x8492, BT_VTYPE_U4)
#define BT_TEST_P05                                             BT_VTPAIR( 0x8493, BT_VTYPE_U4)
#define BT_TEST_P06                                             BT_VTPAIR( 0x8494, BT_VTYPE_D1)
#define BT_TEST_P07                                             BT_VTPAIR( 0x8495, BT_VTYPE_D1)
#define BT_TEST_P08                                             BT_VTPAIR( 0x8496, BT_VTYPE_D2)
#define BT_TEST_P09                                             BT_VTPAIR( 0x8497, BT_VTYPE_D2)
#define BT_TEST_P10                                             BT_VTPAIR( 0x8498, BT_VTYPE_D4)
#define BT_TEST_P11                                             BT_VTPAIR( 0x8499, BT_VTYPE_D4)
#define BT_TEST_P12                                             BT_VTPAIR( 0x849A, BT_VTYPE_U2_FP10)
#define BT_TEST_P13                                             BT_VTPAIR( 0x849B, BT_VTYPE_U2_FP10)
#define BT_TEST_P14                                             BT_VTPAIR( 0x849C, BT_VTYPE_U2_FP100)
#define BT_TEST_P15                                             BT_VTPAIR( 0x849D, BT_VTYPE_U2_FP100)
#define BT_TEST_P16                                             BT_VTPAIR( 0x849E, BT_VTYPE_D2_FP10)
#define BT_TEST_P17                                             BT_VTPAIR( 0x849F, BT_VTYPE_D2_FP10)
#define BT_TEST_P18                                             BT_VTPAIR( 0x84A0, BT_VTYPE_D2_FP100)
#define BT_TEST_P19                                             BT_VTPAIR( 0x84A1, BT_VTYPE_D2_FP100)
#define BT_TEST_P20                                             BT_VTPAIR( 0x84A2, BT_VTYPE_TEXT)
#define BT_TEST_P21                                             BT_VTPAIR( 0x84A3, BT_VTYPE_TEXT)
#define BT_TEST_P22                                             BT_VTPAIR( 0x84A4, BT_VTYPE_DATA)
#define BT_TEST_P23                                             BT_VTPAIR( 0x84A5, BT_VTYPE_DATA)

//-------------------------------------------------------------------------------------------------------------------------

#define BT_PROFILE_PROFILE_NAME                                 BT_VTPAIR( 0x8422, BT_VTYPE_TEXT)
#define BT_PROFILE_CURRENT_PRESET_ASSIGNMENT                    BT_VTPAIR( 0x8464, BT_VTYPE_DATA)
#define BT_PROFILE_NEW_PRESET_ASSIGNMENT                        BT_VTPAIR( 0x8423, BT_VTYPE_DATA)
#define BT_PROFILE_ITCS_REMAINING                               BT_VTPAIR( 0x8A  , BT_VTYPE_U1)
#define BT_PROFILE_HCCS_REMAINING                               BT_VTPAIR( 0x8B  , BT_VTYPE_U1)
#define BT_PROFILE_DHW_TANKS_REMAINING                          BT_VTPAIR( 0x8C  , BT_VTYPE_U1)
#define BT_PROFILE_DEHUMIDIFIERS_REMAINING                      BT_VTPAIR( 0x8D  , BT_VTYPE_U1)
#define BT_PROFILE_DRYING_REMAINING                             BT_VTPAIR( 0x9B  , BT_VTYPE_U1)
#define BT_PROFILE_INTEGRATIONS_REMAINING                       BT_VTPAIR( 0x9C  , BT_VTYPE_U1)
#define BT_PROFILE_CMV_REMAINING                                BT_VTPAIR( 0xE0  , BT_VTYPE_U1)
#define BT_PROFILE_ERR_CONDITIONS_NOT_MET                       BT_VTPAIR( 0x404A, BT_VTYPE_U1)
#define BT_PROFILE_DEHUMIDIFIERS_ALLOCATION                     BT_VTPAIR( 0x8430, BT_VTYPE_DATA)
#define BT_PROFILE_DRYING_ALLOCATION                            BT_VTPAIR( 0x8431, BT_VTYPE_DATA)
#define BT_PROFILE_INTEGRATION_ALLOCATION                       BT_VTPAIR( 0x8432, BT_VTYPE_DATA)
#define BT_PROFILE_HCC_ALLOCATION                               BT_VTPAIR( 0x8463, BT_VTYPE_DATA)
#define BT_PROFILE_CMV_ALLOCATION                               BT_VTPAIR( 0x84A6, BT_VTYPE_DATA)

struct bt_function_preset_assignment {
    uint32_t address;           // Extension unit address (maximum value when free)
    uint8_t preset_id;          // Assigned (extension unit) preset
    uint8_t is_readonly  :1;    // Preset function cannot be changed from user interface
    uint16_t reserved;
};

// Formerly known as sub-profile
enum bt_profile_function_preset {
    BT_PROFILE_PRESET_NONE                              = 0,
    BT_PROFILE_PRESET_MANUAL_DEHUMIDIFIER               = 1,
    BT_PROFILE_PRESET_MANUAL_DEHUMIDIFIER_HC_COIL       = 2,
    BT_PROFILE_PRESET_PS1_1_DEHUMIDIFIER                = 3,
    BT_PROFILE_PRESET_PS1_2_DEHUMIDIFIER                = 4,
    BT_PROFILE_PRESET_PS1_3_DEHUMIDIFIER                = 5,
    BT_PROFILE_PRESET_PS1_4_DEHUMIDIFIER                = 6,
    BT_PROFILE_PRESET_PS2_1_DEHUMIDIFIER_HC_COIL        = 7,
    BT_PROFILE_PRESET_PS2_2_DEHUMIDIFIER_HC_COIL        = 8,
    BT_PROFILE_PRESET_PS2_3_DEHUMIDIFIER_HC_COIL        = 9,
    BT_PROFILE_PRESET_PS3_1_HCC                         = 10,
    BT_PROFILE_PRESET_PS4_1_EDEV_CMV_CLIMATIX_S300      = 11,
    BT_PROFILE_PRESET_ROOM_NO_TEMP_SOURCES              = 12,
    BT_PROFILE_PRESET_PS5_1_EDEV_CMV_TITON              = 13,
	BT_PROFILE_PRESET_MANUAL_GENERIC_VENTILATION        = 14,
	BT_PROFILE_PRESET_PS6_1_GENERIC_VENTILATION         = 15,
};


//-------------------------------------------------------------------------------------------------------------------------

#define BT_AGGREGATED_EDEV_MVDI_PUMP_DEMAND                     BT_VTPAIR( 0xA3  , BT_VTYPE_U1)


//-------------------------------------------------------------------------------------------------------------------------

#define BT_INPUT_VALUE                                          BT_VTPAIR( 0x4A  , BT_VTYPE_D2_FP100)
#define BT_INPUT_VALUE_OVERRIDE                                 BT_VTPAIR( 0x8146, BT_VTYPE_D2_FP100)
#define BT_INPUT_OWNER_OID                                      BT_VTPAIR( 0xAB  , BT_VTYPE_U4)

typedef enum
{
    BT_INPUT_SUBTYPE_PROFILE_TEMPERATURE,
    BT_INPUT_SUBTYPE_PROFILE_PWM,

    // From 128 starts profile variants of all the sub-types
    BT_INPUT_SUBTYPE_TEMPERATURE            = BT_INPUT_SUBTYPE_PROFILE_TEMPERATURE | (1 << 7),
    BT_INPUT_SUBTYPE_PWM                    = BT_INPUT_SUBTYPE_PROFILE_PWM | (1 << 7),
} bt_input_subtype_t;

//-------------------------------------------------------------------------------------------------------------------------

#define BT_INTERFACE_ERR_POWER_SHORTED                          BT_VTPAIR( 0x401C, BT_VTYPE_U1)
#define BT_INTERFACE_MODE                                       BT_VTPAIR( 0x8035, BT_VTYPE_ENUM)

#define BT_INTERFACE_ETH_MAC_ADDRESS                            BT_VTPAIR( 0x8472, BT_VTYPE_DATA)
#define BT_INTERFACE_ETH_IP_CONFIG                              BT_VTPAIR( 0x8473, BT_VTYPE_U1)
#define BT_INTERFACE_ETH_IP_ADDRESS                             BT_VTPAIR( 0xB6  , BT_VTYPE_U4)
#define BT_INTERFACE_ETH_SUBNET_MASK                            BT_VTPAIR( 0xB7  , BT_VTYPE_U4)
#define BT_INTERFACE_ETH_DEFAULT_GATEWAY                        BT_VTPAIR( 0xB8  , BT_VTYPE_U4)
#define BT_INTERFACE_ETH_DHCP_LEASE_TIME                        BT_VTPAIR( 0xAE  , BT_VTYPE_U4)
#define BT_INTERFACE_ETH_STATIC_IP_ADDRESS                      BT_VTPAIR( 0x8474, BT_VTYPE_U4)
#define BT_INTERFACE_ETH_STATIC_SUBNET_MASK                     BT_VTPAIR( 0x8475, BT_VTYPE_U4)
#define BT_INTERFACE_ETH_STATIC_DEFAULT_GATEWAY                 BT_VTPAIR( 0x8476, BT_VTYPE_U4)
#define BT_INTERFACE_ETH_SERVICE_MASK                           BT_VTPAIR( 0x84D9, BT_VTYPE_U4)

#define BT_INTERFACE_MODBUS_MODE                                BT_VTPAIR( 0x8035, BT_VTYPE_ENUM)
#define BT_INTERFACE_MODBUS_ADDR                                BT_VTPAIR( 0x8036, BT_VTYPE_U1)
#define BT_INTERFACE_MODBUS_BAUDRATE                            BT_VTPAIR( 0x8037, BT_VTYPE_U4)
#define BT_INTERFACE_MODBUS_PARITY                              BT_VTPAIR( 0x8420, BT_VTYPE_ENUM)
#define BT_INTERFACE_MODBUS_STOP_BITS                           BT_VTPAIR( 0x8421, BT_VTYPE_ENUM)
#define BT_INTERFACE_MODBUS_PASSWORD                            BT_VTPAIR( 0x814B, BT_VTYPE_U2)

#define BT_INTERFACE_MODBUS_SLAVE_SELECT                        BT_VTPAIR( 0xC0  , BT_VTYPE_U1)
#define BT_INTERFACE_MODBUS_REGISTER_SELECT                     BT_VTPAIR( 0xC1  , BT_VTYPE_U2)
#define BT_INTERFACE_MODBUS_REGISTER_TYPE                       BT_VTPAIR( 0xC2  , BT_VTYPE_U1)
#define BT_INTERFACE_MODBUS_REGISTER_COUNT                      BT_VTPAIR( 0xDD  , BT_VTYPE_U1)
#define BT_INTERFACE_MODBUS_REGISTER_READ                       BT_VTPAIR( 0xC3  , BT_VTYPE_DATA)
#define BT_INTERFACE_MODBUS_REGISTER_WRITE                      BT_VTPAIR( 0xC4  , BT_VTYPE_DATA)

#define BT_INTERFACE_USB_STATE                                  BT_VTPAIR( 0x103 , BT_VTYPE_ENUM)
#define BT_INTERFACE_USB_LOG_MASK                               BT_VTPAIR( 0x84E1, BT_VTYPE_U4)
#define BT_INTERFACE_USB_LOG_PERIOD                             BT_VTPAIR( 0x84E2, BT_VTYPE_D2_FP100)
#define BT_INTERFACE_USB_NEW_FIRMWARE                           BT_VTPAIR( 0x110,  BT_VTYPE_U2)

#define BT_INTERFACE_OPENTHERM_STATE                            BT_VTPAIR( 0x104 , BT_VTYPE_ENUM)
#define BT_INTERFACE_OPENTHERM_HEAT_REQUEST                     BT_VTPAIR( 0x10A , BT_VTYPE_D2_FP100)

#define BT_GUI_BRIGHTNESS                                       BT_VTPAIR( 0x84EE, BT_VTYPE_U1)

enum bt_interface_eth_ip_config {
    BT_INTERFACE_ETH_IP_CONFIG_DYNAMIC,			// IP address, Subnet mask, default gateway and DNS is
                                            // retrieved from DHCP server.
    BT_INTERFACE_ETH_IP_CONFIG_STATIC,			// Values stored in IP address, Subnet mask, default
                                            // gateway and DNS address are used.
};

enum bt_interface_eth_service_mask {
	  BT_INTERFACE_ETH_SERVICE_MODBUS_SLAVE               = 0x800,
};

enum bt_interface_modbus_mode {
    BT_INTERFACE_MODBUS_MODE_DISABLED                   = 0,
    BT_INTERFACE_MODBUS_MODE_SLAVE_READ_ONLY            = 1,
    BT_INTERFACE_MODBUS_MODE_SLAVE_READ_WRITE           = 2,
    BT_INTERFACE_MODBUS_MODE_SLAVE_WRITE_WITH_PASSWORD  = 3,
    BT_INTERFACE_MODBUS_MODE_MASTER                     = 4,
};

enum bt_interface_modbus_register_type {
    BT_INTERFACE_MODBUS_REGISTER_COIL                   = 0,
    BT_INTERFACE_MODBUS_REGISTER_DISCRETE               = 1,
    BT_INTERFACE_MODBUS_REGISTER_INPUT                  = 3,
    BT_INTERFACE_MODBUS_REGISTER_HOLDING                = 4,
};

enum bt_interface_usb_state {
    BT_INTERFACE_USB_STATE_DISABLED                     = 0,
    BT_INTERFACE_USB_STATE_SEARCHING                    = 1,
    BT_INTERFACE_USB_STATE_FLASH_DRIVE                  = 2,
    BT_INTERFACE_USB_STATE_COMMUNICATION                = 3,
};

enum bt_interface_opentherm_state {
    BT_INTERFACE_OPENTHERM_STATE_DISABLED               = 0,
    BT_INTERFACE_OPENTHERM_STATE_IDLE                   = 1,
    BT_INTERFACE_OPENTHERM_STATE_OT_PLUS                = 2,
    BT_INTERFACE_OPENTHERM_STATE_OT_LITE                = 3,
    BT_INTERFACE_OPENTHERM_STATE_RELAY                  = 4,
};

typedef enum
{
    BT_INTERFACE_SUBTYPE_ETHERNET,
    BT_INTERFACE_SUBTYPE_ROXI_BUS,
    BT_INTERFACE_SUBTYPE_RADIO,
    BT_INTERFACE_SUBTYPE_GENERIC_BUS,
    BT_INTERFACE_SUBTYPE_USB,
    BT_INTERFACE_SUBTYPE_OPENTHERM,
} bt_interface_subtype_t;

//-------------------------------------------------------------------------------------------------------------------------


enum bt_week_schedule_interval {
    BT_WEEK_SCHEDULE_INTERVAL_ECO           = 0,
    BT_WEEK_SCHEDULE_INTERVAL_COMFORT       = 1,
    BT_WEEK_SCHEDULE_INTERVAL_EXTRA_COMF    = 2,
    BT_WEEK_SCHEDULE_INTERVAL_FOURTH_VALUE  = 3,

    BT_WEEK_SCHEDULE_TYPE2_INTERVAL_STOPPED     = 0,
    BT_WEEK_SCHEDULE_TYPE2_INTERVAL_UNOCCUPIED  = 1,
    BT_WEEK_SCHEDULE_TYPE2_INTERVAL_ECO         = 2,
    BT_WEEK_SCHEDULE_TYPE2_INTERVAL_COMFORT     = 3,
};

enum bt_week_schedule_type {
    BT_WEEK_SCHEDULE_TYPE_ECO_COMFORT                    = 0,
    BT_WEEK_SCHEDULE_TYPE_ECO_COMFORT_EXTRA              = 1,
    BT_WEEK_SCHEDULE_TYPE_STOPPED_UNOCCUPIED_ECO_COMFORT = 2,
};

struct bt_week_schedule{
    uint16_t kind   :8;         // reserved (compatibility with AC-116)
    uint16_t type   :4;         // enum bt_week_schedule_type
    uint16_t        :4;         // reserved

    uint8_t schedule[7][24];    // enum bt_week_schedule_interval
};

enum bt_calendar_event_pattern {
    BT_CALENDAR_EVENT_PATTERN_EVERY_DAY                 = 0,
    BT_CALENDAR_EVENT_PATTERN_DAY_MASK_IN_EVERY_WEEK    = 1,
    BT_CALENDAR_EVENT_PATTERN_DAY_IN_EVERY_MONTH        = 2
};

struct bt_cal_event
{
    uint16_t minute  :6;
    uint16_t hour    :5;
    uint16_t pattern :5;
    union {
        uint16_t raw;
        struct {
            uint8_t mask:6;
        } day_mask;

        struct {
            uint8_t day :5;
        } day_in_month;
    } pattern_data;
};

struct bt_timespan
{
    uint32_t start_minute :6;
    uint32_t start_hour   :5;

    uint32_t end_minute   :6;
    uint32_t end_hour     :5;
};

struct bt_val_info
{
    uint8_t type;
    uint8_t sub_type;
    uint16_t reserved;
};

#ifdef __cplusplus
extern "C" {
#endif

unsigned bt_val_is_valid(enum bt_vtype val_type, const void *value_or_size);
unsigned bt_val_min_size(enum bt_vtype val_type);
uint32_t bt_invalid_value(enum bt_vtype val_type);
uint8_t bt_device_type(uint32_t address);

STATIC_ASSERT(sizeof(bt_output_indication_override)						== 4, "");
STATIC_ASSERT(sizeof(bt_hcw_status) 									== 4, "");
STATIC_ASSERT(sizeof(bt_drying_demand)									== 4, "");
STATIC_ASSERT(sizeof(bt_drying_status)									== 4, "");
STATIC_ASSERT(sizeof(bt_integration_demand)								== 4, "");
STATIC_ASSERT(sizeof(bt_integration_status)								== 4, "");
STATIC_ASSERT(sizeof(bt_ventilation_state_t) 							== 4, "");
STATIC_ASSERT(sizeof(bt_ventilation_demand) 							== 1, "");
STATIC_ASSERT(sizeof(bt_ventilation_status_t) 							== 4, "");
STATIC_ASSERT(sizeof(struct bt_location_exercising_schedule_override) 	== 8, "");
STATIC_ASSERT(sizeof(struct bt_device_metadata)							== 2, "");
STATIC_ASSERT(sizeof(struct bt_edev_cmv_override)						== 8, "");
STATIC_ASSERT(sizeof(struct bt_edev_cmv_cloud_override) 				== 8, "");
STATIC_ASSERT(sizeof(struct bt_function_preset_assignment) 				== 8, "");
STATIC_ASSERT(sizeof(bt_tmp_ctrl_radiator_srt_control)					== 4, "");
STATIC_ASSERT(sizeof(bt_tmp_ctrl_floor_srt_control)						== 4, "");
STATIC_ASSERT(sizeof(struct bt_cal_event) 								== 4, "");
STATIC_ASSERT(sizeof(struct bt_timespan) 								== 4, "");
STATIC_ASSERT(sizeof(struct bt_week_schedule) 							== 170, "");

#ifdef __cplusplus
}
#endif

#ifdef __cplusplus
#ifndef UNIT_TEST

constexpr int operator "" _degC(long double temp)
{
    return (int)(temp * DegC);
}

constexpr int operator "" _degC(unsigned long long temp)
{
    return temp * DegC;
}

constexpr int operator "" _Volt(long double temp)
{
    return (int)(temp * Volt);
}

constexpr int operator "" _Volt(unsigned long long temp)
{
    return temp * Volt;
}

constexpr int operator "" _Percent(long double temp)
{
    return (int)(temp * Percent);
}

constexpr int operator "" _Percent(unsigned long long temp)
{
    return temp * Percent;
}

constexpr bool operator==(const struct bt_tmp_ctrl_srt_control& lhs, const struct bt_tmp_ctrl_srt_control& rhs)
{
    return *((uint32_t*)&lhs) == *((uint32_t*)&rhs);
}

constexpr bool operator!=(const struct bt_tmp_ctrl_srt_control& lhs, const struct bt_tmp_ctrl_srt_control& rhs)
{
    return !(lhs == rhs);
}


class FunctionPresetAssignment: public bt_function_preset_assignment
{
public:
    FunctionPresetAssignment()
    {
        address = BT_VAL_U4_INVALID;
        preset_id = 0;
        is_readonly = 0;
        reserved = 0;
    }

    bool isAvailable() const
    {
        return address == BT_VAL_U4_INVALID;
    }

    bool hasDeviceAssigned() const
    {
        return address != 0 && address != BT_VAL_U4_INVALID;
    }

    bool operator==(const FunctionPresetAssignment& other) const
    {
        return address == other.address
        && preset_id == other.preset_id
        && is_readonly == other.is_readonly;
    }
};

class EdevCmvOverride: public bt_edev_cmv_override
{
public:
    EdevCmvOverride()
    {
      memset(this, 0, sizeof(*this));
    }

    bool operator>(const EdevCmvOverride& other) const
    {
        // Non has higher priority than the other
        if (priority == 0 && other.priority == 0)
        {
            return false;
        }

        // Valid priority is higher priority
        else if (priority == 0 && other.priority > 0)
        {
            return false;
        }
        else if (other.priority == 0 && priority > 0)
        {
            return true;
        }

        // Lower number has higher priority
        return priority < other.priority;
    }
};

#endif
#endif

#endif /* BT_DATA_H_ */
