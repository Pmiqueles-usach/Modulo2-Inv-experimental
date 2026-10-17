// Multiplicación naive de matrices NxN (Go).
//
// Uso: matmul <salida.csv> <tamaños: 500,1000,1500> <repeticiones> <semilla> [checksum.csv]
//
// Protocolo común a las cuatro implementaciones (ver docs/PROTOCOLO.md):
//   - Matrices float64, almacenamiento plano row-major (slice de N*N).
//   - Generación determinista con SplitMix64 (A primero, luego B), estado reiniciado por cada N.
//   - Algoritmo naive i-j-k con acumulador local.
//   - El temporizador mide SOLO la multiplicación (matrices ya creadas y C ya reservada).
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

// splitMix64 es idéntico en C++, Go, Java y Python.
type splitMix64 struct{ state uint64 }

func (s *splitMix64) next() uint64 {
	s.state += 0x9E3779B97F4A7C15
	z := s.state
	z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9
	z = (z ^ (z >> 27)) * 0x94D049BB133111EB
	return z ^ (z >> 31)
}

// nextDouble devuelve un real uniforme en [0, 1) con 53 bits de precisión.
func (s *splitMix64) nextDouble() float64 {
	return float64(s.next()>>11) * (1.0 / (1 << 53))
}

// generarMatrices genera A y B (en ese orden) a partir de la semilla.
func generarMatrices(n int, semilla uint64) ([]float64, []float64) {
	rng := &splitMix64{state: semilla}
	a := make([]float64, n*n)
	b := make([]float64, n*n)
	for i := range a {
		a[i] = rng.nextDouble()
	}
	for i := range b {
		b[i] = rng.nextDouble()
	}
	return a, b
}

// multiplicar aplica el algoritmo naive i-j-k: C = A x B.
func multiplicar(n int, a, b, c []float64) {
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			suma := 0.0
			for k := 0; k < n; k++ {
				// float64(...) explícito impide la fusión FMA en cualquier arquitectura.
				suma += float64(a[i*n+k] * b[k*n+j])
			}
			c[i*n+j] = suma
		}
	}
}

func checksum(c []float64) float64 {
	s := 0.0
	for _, x := range c {
		s += x
	}
	return s
}

func main() {
	if len(os.Args) < 5 {
		fmt.Fprintln(os.Stderr, "Uso: matmul <salida.csv> <tamaños> <repeticiones> <semilla> [checksum.csv]")
		os.Exit(1)
	}
	salida := os.Args[1]
	var tamanos []int
	for _, t := range strings.Split(os.Args[2], ",") {
		v, err := strconv.Atoi(strings.TrimSpace(t))
		if err != nil {
			panic(err)
		}
		tamanos = append(tamanos, v)
	}
	repeticiones, _ := strconv.Atoi(os.Args[3])
	semilla, _ := strconv.ParseUint(os.Args[4], 10, 64)

	f, err := os.Create(salida)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	csv := bufio.NewWriter(f)
	fmt.Fprintln(csv, "language,N,repetition,time_seconds")

	var chk *bufio.Writer
	if len(os.Args) > 5 {
		fc, err := os.Create(os.Args[5])
		if err != nil {
			panic(err)
		}
		defer fc.Close()
		chk = bufio.NewWriter(fc)
		fmt.Fprintln(chk, "language,N,repetition,checksum,c_first,c_last")
	}

	for _, n := range tamanos {
		a, b := generarMatrices(n, semilla)
		c := make([]float64, n*n)
		for r := 1; r <= repeticiones; r++ {
			inicio := time.Now() // reloj monotónico
			multiplicar(n, a, b, c)
			segundos := time.Since(inicio).Seconds()

			fmt.Fprintf(csv, "go,%d,%d,%.9f\n", n, r, segundos)
			csv.Flush()
			s := checksum(c)
			if chk != nil {
				fmt.Fprintf(chk, "go,%d,%d,%s,%s,%s\n", n, r,
					strconv.FormatFloat(s, 'g', 17, 64),
					strconv.FormatFloat(c[0], 'g', 17, 64),
					strconv.FormatFloat(c[len(c)-1], 'g', 17, 64))
				chk.Flush()
			}
			fmt.Fprintf(os.Stderr, "[go] N=%d rep=%d t=%.6f s checksum=%.6f\n", n, r, segundos, s)
		}
	}
}
