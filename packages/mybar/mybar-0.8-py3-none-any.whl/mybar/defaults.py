field_defs = {

    'hostname': {
        'name': 'hostname',
        'func': field_funcs.get_hostname,
        'run_once': True
    },

    'host': {
        'name': 'host',
        'func': field_funcs.get_host,
        'kwargs': {
            'fmt': '{nodename}',
        },
        'run_once': True
    },

    'uptime': {
        'name': 'uptime',
        'func': field_funcs.get_uptime,
        'setup': _setups.setup_uptime,
        'kwargs': {
            'fmt': '{days}d:{hours}h:{mins}m',
            'sep': ':'
        },
        'icons': [' ', 'Up '],
    },

    'cpu_usage': {
        'name': 'cpu_usage',
        'func': field_funcs.get_cpu_usage,
        'interval': 2,
        'threaded': True,
        'icons': [' ', 'CPU '],
    },

    'cpu_temp': {
        'name': 'cpu_temp',
        'func': field_funcs.get_cpu_temp,
        'interval': 2,
        'threaded': True,
        'icons': [' ', ''],
    },

    'mem_usage': {
        'name': 'mem_usage',
        'func': field_funcs.get_mem_usage,
        'interval': 2,
        'icons': [' ', 'Mem '],
    },

    'disk_usage': {
        'name': 'disk_usage',
        'func': field_funcs.get_disk_usage,
        'interval': 4,
        'icons': [' ', '/:'],
    },

    'battery': {
        'name': 'battery',
        'func': field_funcs.get_battery_info,
        'icons': [' ', 'Bat '],
    },

    'net_stats': {
        'name': 'net_stats',
        'func': field_funcs.get_net_stats,
        'interval': 4,
        'threaded': True,
        'icons': [' ', ''],
    },

    'datetime': {
        'name': 'datetime',
        # 'func': field_funcs.precision_datetime,
        'func': field_funcs.get_datetime,
        'align_to_seconds': True,
        'timely': True,
        'kwargs': {
            'fmt': "%Y-%m-%d %H:%M:%S"
        },
    }

}

field_order = [
    'hostname',
    'uptime',
    'cpu_usage',
    'cpu_temp',
    'mem_usage',
    'disk_usage',
    'battery',
    'net_stats',
    'datetime',
]

bar_params = {
    'separator': '|',
    'refresh_rate': 1.0,
    'field_order': list(_default_field_order)
}

