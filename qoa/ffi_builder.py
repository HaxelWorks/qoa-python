from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef(open("qoa/cffi_def.h").read()) # load the C declarations from the file cdef.h
ffibuilder.set_source("_qoa", open("qoa/qoa.h").read()) # load the C source code from the file qoa.c

if __name__ == "__main__":
    ffibuilder.compile()
