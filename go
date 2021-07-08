clear
echo "Running Postgres..."
echo "conf: "$POSTGRES_CONF
echo "log: "$POSTGRES_LOG
echo "bin: "$POSTGRES_GO
pg_ctl -D $POSTGRES_CONF -l $POSTGRES_LOG -p $POSTGRES_GO start
