from autodox import dox_a_module, dox_a_function, Event, set_after_handler
from tapescript import functions


def process_function_doc(doc: str):
    header = doc.split('\n')[0]
    doc = doc.replace(header, '')
    funcname = header.replace('#', '').strip().split('(')[0]

    if funcname[:4] == '`OP_':
        opname = funcname[1:]
        opcode = functions.opcodes_inverse[opname][0]
        hashtags = header.split(' ')[0]
        header = f'{hashtags} {opname} - {opcode} - x{opcode.to_bytes(1).hex().upper()}'

    return header + doc

def process_module_doc(doc: str):
    # add dox for NOPs
    nops = []
    for name, nop in functions.nopcodes_inverse.items():
        nopdoc = dox_a_function(nop[1], {'format': 'header', 'header_level': 2})
        header = nopdoc.split('\n')[0]
        nopdoc = nopdoc.replace(header, '')
        nopcode = functions.nopcodes_inverse[name][0]
        hashtags = header.split(' ')[0]
        header = f'{hashtags} {name} - {nopcode} - x{nopcode.to_bytes(1).hex().upper()}'
        nops.append(header + nopdoc)
    return doc + ''.join(nops)

set_after_handler(Event.AFTER_FUNCTION, process_function_doc)
set_after_handler(Event.AFTER_MODULE, process_module_doc)

options = {
    'exclude_names': [
        'Tape',
        'annotations',
        'i',
        'sha256',
        'shake_256',
        'ceil',
        'floor',
        'isnan',
        'log2',
        'time',
        'Callable',
        'opcodes',
        'opcodes_inverse',
        'nopcodes',
        'nopcodes_inverse',
        'flags',
        'BadSignatureError',
        'VerifyKey',
        'LifoQueue',
        'tert',
        'yert',
        'vert',
        'sert',
        'token_bytes',
        'bytes_to_int',
        'int_to_bytes',
        'bytes_to_bool',
        'bytes_to_float',
        'float_to_bytes',
    ]
}

# dox_a_module(functions, options)
print(dox_a_module(functions, options))
