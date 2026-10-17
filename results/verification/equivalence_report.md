# Verificación de equivalencia funcional

Se compara el resultado de la multiplicación en cada lenguaje (suma total de C, primer y último elemento). Criterio: igualdad exacta (bit a bit) entre lenguajes y entre repeticiones.

| N | checksum | C[0,0] | C[N-1,N-1] | lenguajes | ¿idénticos? |
|---|---|---|---|---|---|
| 500 | 31283745.652596552 | 129.6193246507308 | 125.49510174050147 | cpp, go, java, python | SÍ |
| 1000 | 250196210.25040233 | 239.53138900135266 | 261.2234877281439 | cpp, go, java, python | SÍ |
| 1500 | 844048831.71274 | 373.6023846907644 | 379.86652101943696 | cpp, go, java, python | SÍ |

**Resultado global:** EQUIVALENTES
