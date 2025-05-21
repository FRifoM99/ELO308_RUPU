#include <stdio.h>

// Definición de la función calculoPIDd
double calculoPIDd(double y, double ref, double *error_ant, double *error_integral, 
                   double kp, double ki, double kd, double limite, 
                   const char* MODO, double out_manual, const char* direccion, 
                   double t_actual, int flag_debug) {
    
    // Modo manual
    if (strcmp(MODO, "MANUAL") == 0) {
        return out_manual;
    }
    
    // Modo automático
    else if (strcmp(MODO, "AUTO") == 0) {
        double error;
        if (strcmp(direccion, "DIRECTO") == 0) {
            error = ref - y;
        } else if (strcmp(direccion, "INVERSO") == 0) {
            error = y - ref;
        }

        // Actualizar el error integral
        error_integral[0] += error * t_actual;
        printf("error integral antes de saturar: %f\n", error_integral[0]);
        if (error_integral[0] * ki > limite) {
            error_integral[0] = limite / ki;
        } else if (ki * error_integral[0] < -limite) {
            error_integral[0] = -limite / ki;
        }

        // Calcular la salida
        double u = kp * error + error_integral[0] * ki + kd * (error - error_ant[0]) / t_actual;

        if (flag_debug) {
            printf("u: %f\n", u);
        }

        // Actualizar el error anterior
        error_ant[0] = error;

        // Limitar la salida
        if (u > (limite * 1.1 + 1)) {
            return limite * 1.1 + 1;
        } else if (u < (limite * 0.9 - 1)) {
            return limite * 0.9 - 1;
        } else {
            return u;
        }
    }

    return 0.0;
}
