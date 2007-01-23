/*******************************************************************************
* test_enzLoCuM4.c
* Pete Owens 2-12-05
* Simulate an ENZ LoCuM-4 low current monitor  
*/

#include "vxWorks.h"
#include "taskLib.h"
#include "a_out.h"
#include <time.h>
#include <sys/times.h>

#include "ioLib.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "ctype.h"
#include "errno.h"
#include "math.h"

#ifdef ABOVE_EPICS_R3_13
#include "recGbl.h"
#include "epicsExport.h"
#endif

#define PLUS_MINUS '\xb1'
#define MU '\xb5'

typedef enum enzLoCuM4Query {
    QUERY_NONE,
    QUERY_CONF,
    QUERY_ERR,
    QUERY_VERS,
    QUERY_COMP,
    QUERY_SET_COMP,
    QUERY_ADR,
    QUERY_INTL,
    QUERY_NEW_INTL,
    QUERY_IDN,
    QUERY_CLS,
    QUERY_RST,
    QUERY_PEAK_A,
    QUERY_PEAK_B,
    QUERY_PEAK_C,
    QUERY_PEAK_D,
    QUERY_ERROR
} QUERY;

typedef enum enzLoCuM4Channel {
    CHAN_A = 0,
    CHAN_B = 1,
    CHAN_C = 2,
    CHAN_D = 3
} CHAN;

char *enzLoCuM4BiasSource = "0Volt";
char *enzLoCuM4Range      = "1mA";
int   enzLoCuM4RangeBit   = (1<<7);
char *enzLoCuM4Version    = "2.34";
int   enzLoCuM4Window     = 16;
int   enzLoCuM4Peak[4]    = {1000, 2000, 3000, 4000};
int   enzLoCuM4High[4]    = {9801, 9802, 9803, 9804};
int   enzLoCuM4Low[4]     = {801,  802,  803,  804 };
char  enzLoCuM4CompReply[50];
int   enzLoCuM4HV         = TRUE;
int   enzLoCuM4Ext        = TRUE;
int   enzLoCuM4Bias       = TRUE;
int   enzLoCuM4Auto       = FALSE;
int   enzLoCuM4Polarity   = TRUE;
int   enzLoCuM4MSB        = TRUE;
int   enzLoCuM4LSB        = TRUE;
int   enzLoCuM4LED        = TRUE;
int   enzLoCuM4AGT        = FALSE;
int   enzLoCuM4BGT        = FALSE;
int   enzLoCuM4CGT        = FALSE;
int   enzLoCuM4DGT        = FALSE;
int   enzLoCuM4ALT        = FALSE;
int   enzLoCuM4BLT        = FALSE;
int   enzLoCuM4CLT        = FALSE;
int   enzLoCuM4DLT        = FALSE;
int   enzLoCuM4Debug      = FALSE;

/*******************************************************************************
* enzLoCuM4Get       get a single command
*/
int enzLoCuM4Get (int fd, char *c)
{
    *c = '\0';
    do {
        if (read (fd, c, 1) != 1)
        {
            if (enzLoCuM4Debug)
                printf ("enzLoCuM4Get: failed to read\n");
            return ERROR;
        }
    } while (*c++ != '\r');
    *c = '\0';
    return OK;
}
/*******************************************************************************
* enzLoCuM4Parse       parse a single command
*/
int enzLoCuM4Parse (char *c, QUERY *q)
{
    int *lim = enzLoCuM4High;
    int i = 1;
    int j = 0;
    int n = 0;

    *q = QUERY_NONE;
    /*
    * Check address
    */
    if (strncmp (c, "$01", 3) != 0)
    {
        if (enzLoCuM4Debug)
            printf ("enzLoCuM4Parse: Bad address %s\n", c);
        return ERROR;
    }

    switch (c[3])
    {
        case ':' :
            /* 
            * Configuration 
            */
            if (strncmp (c+4, "CONF", 4) == 0)
            {
                /*
                * Query configuration 
                */
                if (c[8] =='?')
                {
                    *q = QUERY_CONF;
                    return OK;
                }

                /*
                * Configure measuring range 
                */
                else if (strncmp (c+8, ":CURR:DC", 8) == 0)
                {
                    if (enzLoCuM4Debug) 
                        printf ("enzLoCuM4Parse: Configure measuring range: %s\n", c+17);
                    if (strncmp (c+17, "1E-03", 5) == 0 ||
                        strncmp (c+17, "MAX", 3)   == 0   )
                    {
                        enzLoCuM4Range = "1mA";
                        enzLoCuM4RangeBit = 1 << 7;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-04", 5) == 0)
                    {
                        enzLoCuM4Range = "100_A";
                        enzLoCuM4Range[3] = MU;
                        enzLoCuM4RangeBit = 1 << 6;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-05", 5) == 0)
                    {
                        enzLoCuM4Range = "10_A";
                        enzLoCuM4Range[2] = MU;
                        enzLoCuM4RangeBit = 1 << 5;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-06", 5) == 0)
                    {
                        enzLoCuM4Range = "1_A";
                        enzLoCuM4Range[1] = MU;
                        enzLoCuM4RangeBit = 1 << 4;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-07", 5) == 0)
                    {
                        enzLoCuM4Range = "100nA";
                        enzLoCuM4RangeBit = 1 << 3;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-08", 5) == 0)
                    {
                        enzLoCuM4Range = "10nA";
                        enzLoCuM4RangeBit = 1 << 2;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-09", 5) == 0)
                    {
                        enzLoCuM4Range = "1nA";
                        enzLoCuM4RangeBit = 1 << 1;
                        return OK;
                    }
                    else if (strncmp (c+17, "1E-10", 5) == 0 ||
                             strncmp (c+17, "MIN", 3)   == 0   )
                    {
                        enzLoCuM4Range = "100pA";
                        enzLoCuM4RangeBit = 1 << 0;
                        return OK;
                    }
                    else if (strncmp (c+17, "DEF", 3) == 0)
                    {
                        enzLoCuM4Range = "Auto";
                        enzLoCuM4RangeBit = 0;
                        return OK;
                    }
                }

                /* 
                * Select external bias source 
                */
                else if (strncmp (c+8, ":BIAS:SOURCE", 12) == 0)
                {
                    if (enzLoCuM4Debug) 
                        printf ("enzLoCuM4Parse: Select external bias source: %s\n", c+21);
                    if (strncmp (c+21, "PLUS", 4) == 0)
                    {
                        enzLoCuM4BiasSource = "Plus";
                        return OK;
                    }
                    else if (strncmp (c+21, "MINUS", 5) == 0)
                    {
                        enzLoCuM4BiasSource = "Minus";
                        return OK;
                    }
                    else if (strncmp (c+21, "EXT", 3) == 0)
                    {
                        enzLoCuM4BiasSource = "Ext";
                        return OK;
                    }
                    else if (strncmp (c+21, "DEF", 3) == 0)
                    {
                        enzLoCuM4BiasSource = "0Volt";
                        return OK;
                    }
                }
            }

            /* 
            * System-related commands 
            */
            else if (strncmp (c+4, "SYST", 4) == 0)
            {
                /*
                * Error Status
                */
                if (strncmp (c+8, ":ERR?", 5) == 0)
                {
                    *q = QUERY_ERR;
                    return OK;
                }

                /*
                * Local control
                */
                if (strncmp (c+8, ":LOC", 4) == 0)
                {
                    if (enzLoCuM4Debug) 
                        printf ("enzLoCuM4Parse: Local Control (ignored)\n");
                    return OK;
                }

                /*
                * Version
                */
                if (strncmp (c+8, ":VERS?", 6) == 0)
                {
                    *q = QUERY_VERS;
                    return OK;
                }

                /*
                * Limits
                */
                if (strncmp (c+8, ":COMP", 5) == 0)
                {
                    if (c[13] == '?')
                    {
                        *q = QUERY_COMP;
                        return OK;
                    }
                    else if (c[13] == ':')
                    {
                        if (strncmp (c+14, "HI", 2) == 0)
                            lim = enzLoCuM4High;
                        else if (strncmp (c+14, "LO", 2) == 0)
                            lim = enzLoCuM4Low;
                        else
                            break;

                        if (strncmp (c+16, ":CHA", 4) == 0)
                           i = j = CHAN_A;
                        else if (strncmp (c+16, ":CHB", 4) == 0)
                           i = j = CHAN_B;
                        else if (strncmp (c+16, ":CHC", 4) == 0)
                           i = j = CHAN_C;
                        else if (strncmp (c+16, ":CHD", 4) == 0)
                           i = j = CHAN_D;
                        else if (strncmp (c+16, ":ALL", 4) == 0)
                        {
                           i = CHAN_A;
                           j = CHAN_D;
                        }
                        else
                            break;

                        if (sscanf (c+21, "%d\r", &n) == 1)
                        {
                            if (enzLoCuM4Debug) 
                                 printf ("Setting Limit to %d\n", n);

                            while (i <= j)
                                lim[i++] = n;

                            *q = QUERY_SET_COMP;
                            strcpy (enzLoCuM4CompReply, c);
                            strcat (enzLoCuM4CompReply, "\r");

                            return OK;
                        }
                    }
                }

                /*
                * Address
                */
                if (strncmp (c+8, ":ADR", 4) == 0)
                {
                    if (enzLoCuM4Debug) 
                        printf ("enzLoCuM4Parse: Address (ignored)\n");

                    *q = QUERY_ADR;
                    return OK;
                }

                /*
                * Integration Window
                */
                if (strncmp (c+8, ":INTL", 5) == 0)
                {
                    if (c[13] == '?')
                    {
                        *q = QUERY_INTL;
                        return OK;
                    }

                    if (enzLoCuM4Debug) 
                        printf ("enzLoCuM4Parse: Set Integration Widow: %s\n", c+14);

                    if (sscanf (c+14, "%d", &n) == 1)
                    {
                        switch (n)
                        {
                            case 4: case 8: case 16: case 32: case 64:
                                *q = QUERY_NEW_INTL;
                                enzLoCuM4Window = n;
                                return OK;
                            default:
                                *q = QUERY_ERROR;
                                return OK;
                        }
                    }
                }
            }

            /*
            * Rectified channel peak values 
            */
            else if (strncmp (c+4, "MEAS:CH", 7) == 0)
            {
                if (c[11] == 'A')
                {
                    *q = QUERY_PEAK_A;
                    return OK;
                }
                if (c[11] == 'B')
                {
                    *q = QUERY_PEAK_B;
                    return OK;
                }
                if (c[11] == 'C')
                {
                    *q = QUERY_PEAK_C;
                    return OK;
                }
                if (c[11] == 'D')
                {
                    *q = QUERY_PEAK_D;
                    return OK;
                }
            }

        case '*' :
            /*
            * Read Identifiaction string 
            */
            if (strncmp (c+4, "IDN?", 4) == 0)
            {
                *q = QUERY_IDN;
                return OK;
            }

            /* 
            * Reset Device 
            */
            else if (strncmp (c+4, "RST", 3) == 0)
            {
                if (enzLoCuM4Debug) 
                    printf ("enzLoCuM4Parse: System Reset\n");

                *q = QUERY_RST;
                enzLoCuM4BiasSource = "0Volt";
                enzLoCuM4Range = "1mA";
                return OK;
            }

            /* 
            * Query Status
            */
            else if (strncmp (c+4, "CLS", 3) == 0)
            {
                *q = QUERY_CLS;
                return OK;
            }
    }

    if (enzLoCuM4Debug) 
        printf ("enzLoCuM4Parse: Bad command %s\n", c);

    return ERROR;
}
/*******************************************************************************
* enzLoCuM4Reply       Simulate an ENZ LoCuM-4 low current monitor
*/
int enzLoCuM4Reply (int fd, QUERY q)
{
    char reply[80];
    char *r;

    switch (q)
    {
        default:
            if (enzLoCuM4Debug) 
                printf ("Unknown Query %d\n", q);
            return ERROR;
        case QUERY_NONE:
            return OK;
        case QUERY_CONF:
            sprintf (reply, "S1_%s,S2_%s,HV_%s,Ext_%s,Bias\xb1_%s,Auto_%s\r", 
                             enzLoCuM4Range, 
                             enzLoCuM4BiasSource, 
                             enzLoCuM4HV   ? "ON" : "OFF", 
                             enzLoCuM4Ext  ? "ON" : "OFF", 
                             enzLoCuM4Bias ? "ON" : "OFF", 
                             enzLoCuM4Auto ? "ON" : "OFF");
            break;
        case QUERY_ERR:
            strcpy (reply, "No_Error\r");
            break;
        case QUERY_VERS:
            sprintf (reply, "SCPI_ENZ_%s\r", enzLoCuM4Version);
            break;
        case QUERY_COMP:
            sprintf (reply, "ChD %04d,%04d\rChC %04d,%04d\rChB %04d,%04d\rChA %04d,%04d\r", 
                            enzLoCuM4High[3], enzLoCuM4Low[3], 
                            enzLoCuM4High[2], enzLoCuM4Low[2], 
                            enzLoCuM4High[1], enzLoCuM4Low[1], 
                            enzLoCuM4High[0], enzLoCuM4Low[0] );
            break;
        case QUERY_SET_COMP:
            strcpy (reply, enzLoCuM4CompReply);
            break;
        case QUERY_ADR:
            strcpy (reply, "Err\r");
            break;
        case QUERY_INTL:
              sprintf (reply, "MVSL: %d\r", enzLoCuM4Window);
            break;
        case QUERY_NEW_INTL:
              sprintf (reply, "New INTL: %d\r", enzLoCuM4Window);
            break;
        case QUERY_IDN:
            sprintf (reply, "LoCuM4,Version %s,Address 01,#12345\r", enzLoCuM4Version);
            break;
        case QUERY_CLS:
            sprintf (reply, "P3_P4_P0:\rXXYYZZ\r");
            reply[10] = ((enzLoCuM4Ext      << 3 | 
                          enzLoCuM4Polarity << 2 |
                          enzLoCuM4Bias     << 1 |
                          enzLoCuM4HV       << 0 ) & 0xf) + '0';
            reply[11] = ((enzLoCuM4Auto     << 3 | 
                          enzLoCuM4MSB      << 2 |
                          enzLoCuM4LED      << 1 |
                          enzLoCuM4LSB      << 0 ) & 0xf) + '0';
            reply[12] = ((enzLoCuM4RangeBit >> 4 ) & 0xf) + '0';
            reply[13] = ((enzLoCuM4RangeBit      ) & 0xf) + '0';
            reply[14] = ((enzLoCuM4AGT      << 3 | 
                          enzLoCuM4BGT      << 2 |
                          enzLoCuM4CGT      << 1 |
                          enzLoCuM4DGT      << 0 ) & 0xf) + '0';
            reply[15] = ((enzLoCuM4ALT      << 3 | 
                          enzLoCuM4BLT      << 2 |
                          enzLoCuM4CLT      << 1 |
                          enzLoCuM4DLT      << 0 ) & 0xf) + '0';
            break;
        case QUERY_RST:
            strcpy (reply, "Reset\r");
            break;
        case QUERY_ERROR:
            strcpy (reply, "Err\r");
            break;
        case QUERY_PEAK_A:
            sprintf (reply, "CHA %d\r", enzLoCuM4Peak[CHAN_A]);
            break;
        case QUERY_PEAK_B:
            sprintf (reply, "CHB %d\r", enzLoCuM4Peak[CHAN_B]);
            break;
        case QUERY_PEAK_C:
            sprintf (reply, "CHC %d\r", enzLoCuM4Peak[CHAN_C]);
            break;
        case QUERY_PEAK_D:
            sprintf (reply, "CHD %d\r", enzLoCuM4Peak[CHAN_D]);
            break;
    }

    taskDelay (6);
    write (fd, reply, strlen (reply));

    if (enzLoCuM4Debug)
    {
        printf ("REPLY:\n");
        for (r = reply; *r; r++)
        {
            switch (*r)
            {
                case '\r':       printf ("<CR>\n"); break;
                case MU:         printf ("<MU>");   break;
                case PLUS_MINUS: printf ("<+->");   break;
                default:         printf ("%c", *r);
            }
        }
    }

    return OK;
}
/*******************************************************************************
* enzLoCuM4Simulate       Simulate an ENZ LoCuM-4 low current monitor
*/
void enzLoCuM4Simulate (char *port)
{
    int  fd = open (port, O_RDWR, 0);
    char command[30];
    QUERY query;

    for (;;)
    {
        if (enzLoCuM4Get (fd, command) != OK)
            continue;
        if (enzLoCuM4Debug)
            printf ("\nREAD %s\n", command);
        if (enzLoCuM4Parse (command, &query) != OK)
            continue;
        enzLoCuM4Reply (fd, query);
    }
}
/*******************************************************************************
* enzLoCuM4Splat       a test function
*/
void enzSplat (char *port)
{
    int  fd = open (port, O_WRONLY, 0);
taskDelay (600);
/*
    for (;;)
    {
*/
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:CURR:DC MAX\r", 21);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:CURR:DC 1E-03\r", 23);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:CURR:DC 1E-04\r", 23);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:CURR:DC 1E-05\r", 23);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:CURR:DC 1E-06\r", 23);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:CURR:DC 1E-07\r", 23);
        write (fd, "$01:CONF:CURR:DC 1E-08\r", 23);
        write (fd, "$01:CONF:CURR:DC 1E-09\r", 23);
        write (fd, "$01:CONF:CURR:DC 1E-10\r", 23);
        write (fd, "$01:CONF:CURR:DC DEF\r", 21);
        write (fd, "$01:CONF:CURR:DC MIN\r", 21);
        write (fd, "$01:CONF:BIAS:SOURCE PLUS\r", 26);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:BIAS:SOURCE MINUS\r", 27);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:BIAS:SOURCE DEF\r", 25);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:BIAS:SOURCE EXT\r", 25);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01:CONF:BIAS:SOURCE XXX\r", 25);
        write (fd, "$01:SYST\r", 9);
        write (fd, "$01:SYST:ERR?\r", 14);
        write (fd, "$01:SYST:VERS?\r", 15);
        write (fd, "$01:SYST:LOC\r", 13);
        write (fd, "$01:SYST:COMP:HI:ALL 9999\r", 26);
        write (fd, "$01:SYST:COMP:LO:ALL 1111\r", 26);
        write (fd, "$01:SYST:COMP:HI:CHA 1234\r", 26);
        write (fd, "$01:SYST:COMP:LO:CHB 0001\r", 26);
        write (fd, "$01:SYST:COMP:HI:XXX 1111\r", 26);
        write (fd, "$01:SYST:COMP?\r", 15);
        write (fd, "$01:SYST:INTL?\r", 15);
        write (fd, "$01:SYST:INTL 41\r", 17);
        write (fd, "$01:SYST:INTL?\r", 15);
        write (fd, "$01:SYST:INTL 4\r", 16);
        write (fd, "$01:SYST:INTL?\r", 15);
        write (fd, "$01:MEAS\r", 9);
        write (fd, "$01*IDN?\r", 9);
        write (fd, "$01*RST\r", 8);
        write (fd, "$01:CONF?\r", 10);
        write (fd, "$01*CLS\r", 8);
/*
        taskDelay (60);
    }
*/
}
void chars ()
{
char i;
for (i=0;i<0xff;i++)
printf ("%02x : %c\n",i,i);
}
/*******************************************************************************
*/
#ifdef ABOVE_EPICS_R3_13
/* No functions currently registered ... */
/* epicsRegisterFunction(); */
#endif


