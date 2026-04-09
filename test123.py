
file=$(find /productos/sproxy/SSP -type f -name 'sftp.adapter-SFTP_E02_1724*.log' | sort | tail -1)
echo "$file"
grep -nE 'SSE1800I|SSE1831E|SSP0331E|SSP0332I|SSP0339W|SSP0340I|SSE1811E|SSE1814E' "$file" | fold -s -w 180


find /productos/sproxy/SSP -type f -name '*.log' -print0 |
xargs -0 grep -nE 'SSE1800I|SSE1831E|SSP0331E|SSP0332I|SSP0339W|SSP0340I|SSE1811E|SSE1814E' 2>/dev/null |
grep 'SFTP_E02_1724\|HOST2_SEAS' | fold -s -w 180
