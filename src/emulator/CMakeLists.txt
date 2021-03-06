include_directories(${FAASM_INCLUDE_DIR}/emulator)

set(PUBLIC_HEADERS
        ${FAASM_INCLUDE_DIR}/emulator/emulator.h
        ${FAASM_INCLUDE_DIR}/emulator/emulator_api.h
)
set(LIB_FILES emulator.cpp)

faasm_public_lib(emulator "${LIB_FILES}")
set_target_properties(emulator PROPERTIES PUBLIC_HEADER "${PUBLIC_HEADERS}")


if (FAASM_BUILD_TYPE STREQUAL "native-tools")
    target_link_libraries(emulator faasm scheduler state)
else ()
    target_link_libraries(emulator scheduler state)
endif ()

install(TARGETS emulator
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        PUBLIC_HEADER DESTINATION include/faasm
        )
