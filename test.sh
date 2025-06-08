if JobStep "Section 1: Truncate and load PWK_TEAM_ MBR" ; then
stamp "Section 1.1: Truncate table PWK_TEAM MBR" »> $10g
SqlTrunc -d oracle -u d_etl -t PWK_TEAM_MBR - 1 $10g
fi

if JobStep "Section 2: Collecting Statistics on PWK_TEAM_MBR table" ; then
Sqlstats -d oracle -u dm_etl -t PWK_TEAM_MBR - 1 $10g
db2_connect
fi

#if JobStep "Section 3: Update TEAM_MBR from PWK_TEAM MBR " ; then
#sort -t <xxxxxxxx>fi
#fi

if JobStep "Section 4: Update TEAM_MBRA from PWK_TEAM MBR " ; then
ls-ltr-t <xxxxxxxx>fi
getfilebypass
ChunkSql
initialize_environment
db2_connect
fi

if JobStep "Section 5: Update TEAM_MBAR from PWK_TEAM MBR " ; then
ls-ltr-t <xxxxxxxx>fi5

fi
if JobStep "Section 6: Update TEAM_MBR from PWK_TEAM MBR " ; then
ls-ltr-t <xxxxxxxx>fi
save_to_bdi_
bdi_cleanup
notify_bdi_
fi