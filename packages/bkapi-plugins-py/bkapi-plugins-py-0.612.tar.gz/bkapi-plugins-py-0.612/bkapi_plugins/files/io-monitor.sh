pidstat -d 1 1 | awk 'NR > 2 && ($4 != 0 || $5 != 0) && $3 ~ /^[0-9]+$/ && $1 ~ /Average/ {
  pid = $3;
  cmd = "ps -q " pid " -o comm=";
  cmd | getline process_name;
  close(cmd);
  if (process_name != "") {
    printf "process_io_bytes{pid=\"%s\", process_name=\"%s\", type=\"read\"} %d\n" \
      "process_io_bytes{pid=\"%s\", process_name=\"%s\", type=\"write\"} %d\n" \
      "process_ccwr{pid=\"%s\", process_name=\"%s\"} %.2f\n" \
      "process_iodelay{pid=\"%s\", process_name=\"%s\"} %.2f\n", \
      pid, process_name, $4, pid, process_name, $5, \
      pid, process_name, $6, pid, process_name, $7;
  }
}' | sort -k2 -nr | awk 'NR <= 20 && $2 > 0 { print }'