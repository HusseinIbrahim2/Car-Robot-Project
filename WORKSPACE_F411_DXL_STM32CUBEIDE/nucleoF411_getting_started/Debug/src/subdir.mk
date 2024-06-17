################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/SystemClock.c \
../src/dynamixel.c \
../src/main.c \
../src/stm32f4xx_hal_msp.c \
../src/stm32f4xx_it.c \
../src/syscalls.c \
../src/system_stm32f4xx.c \
../src/tickTimer.c \
../src/util.c 

OBJS += \
./src/SystemClock.o \
./src/dynamixel.o \
./src/main.o \
./src/stm32f4xx_hal_msp.o \
./src/stm32f4xx_it.o \
./src/syscalls.o \
./src/system_stm32f4xx.o \
./src/tickTimer.o \
./src/util.o 

C_DEPS += \
./src/SystemClock.d \
./src/dynamixel.d \
./src/main.d \
./src/stm32f4xx_hal_msp.d \
./src/stm32f4xx_it.d \
./src/syscalls.d \
./src/system_stm32f4xx.d \
./src/tickTimer.d \
./src/util.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o src/%.su src/%.cyclo: ../src/%.c src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DSTM32 -DSTM32F4 -DSTM32F411RETx -DNUCLEO_F411RE -DDEBUG -DSTM32F411xE -DUSE_HAL_DRIVER -c -I"F:/ENIB STUDY/S6O/projet-robot/WORKSPACE_F411_DXL_STM32CUBEIDE/nucleoF411_getting_started/HAL_Driver/Inc/Legacy" -I"F:/ENIB STUDY/S6O/projet-robot/WORKSPACE_F411_DXL_STM32CUBEIDE/nucleoF411_getting_started/Utilities/STM32F4xx-Nucleo" -I"F:/ENIB STUDY/S6O/projet-robot/WORKSPACE_F411_DXL_STM32CUBEIDE/nucleoF411_getting_started/inc" -I"F:/ENIB STUDY/S6O/projet-robot/WORKSPACE_F411_DXL_STM32CUBEIDE/nucleoF411_getting_started/CMSIS/device" -I"F:/ENIB STUDY/S6O/projet-robot/WORKSPACE_F411_DXL_STM32CUBEIDE/nucleoF411_getting_started/CMSIS/core" -I"F:/ENIB STUDY/S6O/projet-robot/WORKSPACE_F411_DXL_STM32CUBEIDE/nucleoF411_getting_started/HAL_Driver/Inc" -O0 -ffunction-sections -Wall -fcommon -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-src

clean-src:
	-$(RM) ./src/SystemClock.cyclo ./src/SystemClock.d ./src/SystemClock.o ./src/SystemClock.su ./src/dynamixel.cyclo ./src/dynamixel.d ./src/dynamixel.o ./src/dynamixel.su ./src/main.cyclo ./src/main.d ./src/main.o ./src/main.su ./src/stm32f4xx_hal_msp.cyclo ./src/stm32f4xx_hal_msp.d ./src/stm32f4xx_hal_msp.o ./src/stm32f4xx_hal_msp.su ./src/stm32f4xx_it.cyclo ./src/stm32f4xx_it.d ./src/stm32f4xx_it.o ./src/stm32f4xx_it.su ./src/syscalls.cyclo ./src/syscalls.d ./src/syscalls.o ./src/syscalls.su ./src/system_stm32f4xx.cyclo ./src/system_stm32f4xx.d ./src/system_stm32f4xx.o ./src/system_stm32f4xx.su ./src/tickTimer.cyclo ./src/tickTimer.d ./src/tickTimer.o ./src/tickTimer.su ./src/util.cyclo ./src/util.d ./src/util.o ./src/util.su

.PHONY: clean-src

