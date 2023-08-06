pidstat -d 1 1 | awk 'NR > 2 && ($4 != 0 || $5 != 0) && $3 ~ /^[0-9]+$/ && $1 ~ /Average/ {
  pid = $3;
  cmd = "ps -q " pid " -o comm= -o user=";
  cmd | getline process_info;
  close(cmd);
  split(process_info, info_array, " ");
  process_name = info_array[1];
  user = info_array[2];
  if (process_name != "") {
    printf "process_io_bytes{pid=\"%s\", process_name=\"%s\", user=\"%s\", type=\"read\"} %d\n" \
      "process_io_bytes{pid=\"%s\", process_name=\"%s\", user=\"%s\", type=\"write\"} %d\n" \
      "process_ccwr{pid=\"%s\", process_name=\"%s\", user=\"%s\"} %.2f\n" \
      "process_iodelay{pid=\"%s\", process_name=\"%s\", user=\"%s\"} %.2f\n", \
      pid, process_name, user, $4, pid, process_name, user, $5, \
      pid, process_name, user, $6, pid, process_name, user, $7;
  }
}' | sort -k2 -nr | awk 'NR <= 20 && $2 > 0 { print }'


