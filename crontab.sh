# Runs the monitor.sh every 30mins and saves the logs in case of error
*/30 * * * * /.../monitor.sh >> /.../monitor.log 2>&1