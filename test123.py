find /productos/sproxy/SSP -type f \( -iname '*.xml' -o -iname '*.properties' -o -iname '*.conf' \) \ -exec grep -nH -E '30406|1724|HOST2_SSP_SEAS_E02_PS01|SFTP_E02_1724' {} + 2>/dev/null


find /productos/sproxy/SSP -type f \( -iname '*.log' -o -iname '*.out' \) \ -exec grep -nH -E '30406|1724|HOST2_SSP_SEAS_E02_PS01|SFTP_E02_1724|SEAS|perimeter|listener|FAIL|ERROR|Exception|timeout|refused|handshake' {} + 2>/dev/null | tail -200

