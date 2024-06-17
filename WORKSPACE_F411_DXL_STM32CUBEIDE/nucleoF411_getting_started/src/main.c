#include "stm32f4xx.h"
#include "stm32f4xx_nucleo.h"

#include "drv_uart.h"
#include "dynamixel.h"
#include <stdio.h>
#include <stdlib.h>

extern uint8_t car_received;
extern uint8_t rec_buf1[1+1];
//extern char speed_received[10];
//extern uint8_t speed_received;
uint8_t v;
char snum[10];
char str[10];
//uint8_t signal_recieved;

int main(void)
{
	HAL_Init();	// passage par stm32f4xx_hal_msp.c : configuration des broches
	SystemClock_Config();

    uart1_Init();			// ZIGBEE
    uart2_Init();           // CABLE
    uart6_Init();           // DYNAMIXEL
    HAL_Delay(500);
    HAL_MspInit();


	  /*Uart6Handle.Instance          = USART6;

	  Uart6Handle.Init.BaudRate     =57600;//1000000;//57600;
	  Uart6Handle.Init.WordLength   = UART_WORDLENGTH_8B;
	  Uart6Handle.Init.StopBits     = UART_STOPBITS_1;
	  Uart6Handle.Init.Parity       = UART_PARITY_NONE;
	  Uart6Handle.Init.HwFlowCtl    = UART_HWCONTROL_NONE;
	  Uart6Handle.Init.Mode         = UART_MODE_TX_RX;
	  Uart6Handle.Init.OverSampling = UART_OVERSAMPLING_16;

	  HAL_UART_Init(&Uart6Handle);*/


	dxl_LED(2, LED_ON);
	dxl_LED(1, LED_ON);
	HAL_Delay(500);
	dxl_LED(1, LED_OFF);
	dxl_LED(2, LED_OFF);
	HAL_Delay(500);
	dxl_LED(1, LED_ON );
	dxl_LED(2, LED_ON );
	HAL_Delay(500);
	dxl_LED(1, LED_OFF);
	dxl_LED(2, LED_OFF);
	HAL_Delay(100);

	/*dxl_setOperatingMode(2, VELOCITY_MODE);
	dxl_setOperatingMode(1, VELOCITY_MODE);
	dxl_torque(2, TORQUE_ON);
	dxl_torque(1, TORQUE_ON);
	dxl_setGoalVelocity(2, -265);
	dxl_setGoalVelocity(1, 265);

	dxl_torque(2, TORQUE_OFF);
	dxl_torque(1, TORQUE_OFF);*/

	dxl_setOperatingMode(1, VELOCITY_MODE);
	dxl_torque(1,TORQUE_ON);

	dxl_setOperatingMode(2, VELOCITY_MODE);
	dxl_torque(2,TORQUE_ON);

	//static int i=50;
	//uint8_t r1 ="";
	//uint8_t rec_buf6[]="";
	//uint8_t r2 ="";
	    while(1)
	    {




	    	v=(uint8_t)rec_buf1[1];
	    	switch(rec_buf1[0])
	    	{
	    	//HAL_Delay(1000);
	    	case 'z':
	    		dxl_setGoalVelocity(1, v);
	    		dxl_setGoalVelocity(2, -v);
	    		//r1="265";
	    		//r2="265;";
	    		//HAL_Delay(1000);
	    		term_printf_zigbee("265,265");
	    		//HAL_Delay(500);
	    		break;
	    	case 's':
	    		dxl_setGoalVelocity(1, -v);
	    		dxl_setGoalVelocity(2, v);
	    		HAL_Delay(500);
	    		term_printf_zigbee("265,265");
	    		HAL_Delay(500);
	    		break;

	    	case 'd':
	    		dxl_setGoalVelocity(1, v);
	    		dxl_setGoalVelocity(2, v);
	    		HAL_Delay(500);
	    		term_printf_zigbee("265,135");
	    		HAL_Delay(500);
	    		break;

	    	case 'q':
	    		dxl_setGoalVelocity(1, -v);
	    		dxl_setGoalVelocity(2, -v);
	    		HAL_Delay(500);
	    		term_printf_zigbee("135,265");
	    		HAL_Delay(500);
	    		break;

	    	case 'h':
	    		dxl_setGoalVelocity(1, 0);
	    		dxl_setGoalVelocity(2, 0);
	    		HAL_Delay(500);
	    		term_printf_zigbee("0,0");
	    		HAL_Delay(500);
	    		break;

	    	case 'c':
	    		if((HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_8)) && (HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_0)))
	    			{
	    		    		dxl_setGoalVelocity(1, 50);
	    		    		dxl_setGoalVelocity(2, -50);

	    		    		    		/*HAL_Delay(500);
	    		    		    		term_printf_zigbee("60,60");

	    		    		    		HAL_Delay(500);*/
	    		   }
	    		  else if((!HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_8)) && (!HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_0)))
	    		   {
	    		    dxl_setGoalVelocity(1, 0);
	    		    dxl_setGoalVelocity(2, 0);

	    		    			    		/*HAL_Delay(500);
	    		    			    		term_printf_zigbee("0,0");
	    		    			    		HAL_Delay(500);*/
	    		}
	    		  else if((!HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_8)) && (HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_0)))
	    		    	   {
	    		    		dxl_setGoalVelocity(1, -50);
	    		    		dxl_setGoalVelocity(2, -50);

	    		    			    		/*HAL_Delay(500);
	    		    			    		term_printf_zigbee("60,60");
	    		    			    		HAL_Delay(500);*/
	    		    	    }
	    		   else if((!HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_0)) && (HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_8)))
	    		    	    {
	    		    			dxl_setGoalVelocity(1, 50);
	    		    			dxl_setGoalVelocity(2, 50);

	    		    			    		/*HAL_Delay(500);
	    		    			    		term_printf_zigbee("60,60");
	    		    			    		HAL_Delay(500);*/
	    		    	    }
	    						break;


	    }
	    HAL_Delay(10); // 100 ms

	   }
	    return 0;
}

//=====================================================================================
