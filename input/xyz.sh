more bdi_dlyoptnsquots10d.sh
#1/bin/ksh
# SCRIPT
: bdi_dlyoptnsquots10d.sh
#
Purpose
Loads the data from flat file odd. quotes.gz to OD_SEC table,
DLY_OPTNS_QUOTS
####萨＃拌#
Input
: omdd. quotes.gz
#
Output
: OD_SEC. DLY_OPTNS_QUOTS
#
#
Frequency : Event based scheduling
#
井#######＃#############################＃＃#######＃##
#＃
#
REVISIONS HISTORY
#######################################################＃#
Date
Developer.
Change
#
P0512812
10/04/2017
TL- Kim Evens
Initial Release
Dev- Sravani Adusumalli
removed sec 1.4
02/14/2023
BCPJ-3111
Vijetha G
added failure to sec 1.2
#＃#＃＃＃＃＃＃并＃＃＃＃＃#＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃我＃＃＃我＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃
SHOME/ profile_bdi
Init -f multi -s bdi_dlyoptnsquots10d
vSrcFile=omdd. quotes. gz
vTgtTable=DLY_OPTNS_QUOTS
APP_ENV= echo SAPPENV | tr "[: lower:]" "[:upper:]"-function MainProcess
if JobStep "Section 1: Get source file from the dropbox and copy to Sdatadir "; then
	"Section 1.1: Get file from the dropbox and copy to Sdatadir " >> $10g
	GetFile -S
	SvSrcFile -t Sdatadir/SvSrcFile $log
	stamp "Section 1.2: Checking
		whether the source file exists">> $log
	if Ul -f Sdatadir/SvSrcFile ]J
		stamp "The source file exist"» 51og
	else
		stamp "The source file does not exist"» $log
 Session
Manager.
Command Manager
Active Sessions
Dev
x
stamp "The source file does not exist"» $log
Checkrc -r 99
fi
stamp "Section 1.3: Check whether the file is empty" »> $log
VFILECHECK= zcat Sdatadir/SvSrcFile | head -1
if [[ -z SvFILECHECK 1!; then
stamp "The source file is empty. " >> $1og emptysrcfile
Checkrc -r 99
fi
fi
if Jobstep "Section 2: Create work table for Exchange Partition"; then
stamp "Section 2:Create work table for Exchange Partition" >› $1og
SqlExecute -u od_sec -t oracle -f $bindir/SvScript.create_tmp_dly_optns_quots.sql -1 $log
fi
if JobStep "Section 3: Powermart to create insert file to load SvTgtTable "; then
stamp "Section 3.1:Use OdControlMaxId for SvTgtTable and SvTgtTable_ID column " » $log
ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID
stamp "Section 3.2: Get current batch date for parm file " » Slog Sq Execute -t oracle -f Sbindir/Svscript.get_date_parm_file.sql -1 $log
"Section 3.3: Create parameter file and pass PROC_DT " > $10g stamp, rUDM_STG. WF:wf_m_dly_optns_quots.ST:s m_dly_optns_quots]"
	⁠Stmpdir/Svscript.param
cat Sdatadir/Sv$cript.get_date_parm_file.txt >> Stmpdir/SvScript. param
"Section 3.4: Calling
the powemart session to create insert file from the Svrcile " > Slog
"Work Flow will be
using the command line to unzip the source file for processing the large amount of records" » $1og
Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 - 1 $10g
stamp " External Loader connection in session will do inserts only. using sqlldr to load TMP_DLY_OPTNS_QUOTS." » $10g
fi
if JobStep "Section 4: Execute exchange partition of TMP_STgtTable SvTgtTable"; then
stamp "Section 4:Execute exchange partition of MP_SvTgtTable $vTgtTable " > $1og
SqlExecute
-u od_sec -t oracle -f Sbindir/SvScript. exchange_partition.sql -1 $log
fi
if Jobstep "Section 5: Drop Temporary work table TMP_DLY_OPTNS_QUOTS"; then stamp "Section 5:Drop Temporary work table TMP_DLY_OPTNS_QUOTS " »> $10g
Ready
if Jobstep "Section 6: Run stats on SvgtTable "; then stamp "Section 6: Run stats on $yTgtTable " »> $10g Sqlstats -u od sec -d oracle -t $vIgtTable
•⁠  ⁠T
$10gger

if Jobstep "Section 7: Purge data older than 7 days "; then stamp "Section 7:Purge data older than 7 days" >> $1og PurgeIntervalPartitions -u od_sec -t SvigtTable -1 $1og

if JobStep " Section 8: Rename the Informatica bad files to include PROC date and move to qltydir"; then
for badfile in Is Sdatadir/Svscript.".bad if [[-s $badfile ]] ; then
vSuffix=
echo $badfile / cut -f2- -d.
my Sbadfile Sqltydir/SvScript. $vLogDt, $vsuffix » $1og
Checkrc -r $?
stamp "BadFile $badfile renamed to $vscript.$vLogDt.$vSuffix" >› $1og
Fi done
fi
if Jobstep "Section 9: Moving Compressed source file to Sarcdir and removing. load file "; then
stamp "Section 9.1:Moving Compressed source file to Sarcdir, " >> $log mv Sdatadir/omdd.quotes.gz Sarcdir/$vScript.$vLogDt. omdd.quotes.gz 2>> $10g
*es 05123 5109
Checkrc -r $?
stamp "Section 9.2:Remove .load From ODS DropBox " >> $10g
RemoveFile -f SvrcFile. load -1 $1og
Checkrc -r $?
fi
if Jobstep "Section 10: Clean-up"; then
stamp "Section 10:Remove log files more than 7 executions " >> $log
CleanUpFiles
CleanUpFiles -d
-s $vScript -1 $1og
CleanUpFiles
-d
-p
Sarcdir -s $vScript -1 $10g
7
CleanUpFiles -d 7 -p
Saltydir -5 Svscript - $10g
Sdatadir -s SvScript -T-$10g
Active Sessions
function emptyscfile
stamp "Send e-mail to notify source file is empty" » $1og stamp
"Removing previous email body temp file" >> $1og
rm -f Stmpdir/SvScript. email
	⁠$10g 2>&1
stamp "Creating 'To' list for
email" » $log
sRecipientsad; /d Scontrol/muscript SAPP ENV. email. cfg > Stmpdir/Svscript. SAPP_ENV. email. cfg
< Stmpdir/$vscript.$APP_ENV. email.cfg
Subject=''#!/bin/ksh

# SCRIPT: bdi_dlyoptnsquots10d.sh
# Purpose: Loads data from flat file omdd.quotes.gz to OD_SEC table, DLY_OPTNS_QUOTS
# Input: omdd.quotes.gz
# Output: OD_SEC.DLY_OPTNS_QUOTS
# Frequency: Event-based scheduling

# REVISIONS HISTORY
# Date        Developer        Change
# 10/04/2017  TL- Kim Evens    Initial Release
# 02/14/2023  Vijetha G        Added failure check to section 1.2 (BCPJ-3111)

. $HOME/profile_bdi
Init -f multi -s bdi_dlyoptnsquots10d

vSrcFile="omdd.quotes.gz"
vTgtTable="DLY_OPTNS_QUOTS"
APP_ENV=$(echo SAPPENV | tr '[:lower:]' '[:upper:]')

function MainProcess {
    if JobStep "Section 1: Get source file from the dropbox and copy to Sdatadir"; then
        stamp "Section 1.1: Get file from the dropbox and copy to Sdatadir" >> $log
        GetFile -S
        SvSrcFile -t Sdatadir/SvSrcFile $log

        stamp "Section 1.2: Checking whether the source file exists" >> $log
        if [[ -f Sdatadir/SvSrcFile ]]; then
            stamp "The source file exists" >> $log
            db_chunk_size
        else
            stamp "The source file does not exist" >> $log
            Checkrc -r 99
        fi

        stamp "Section 1.3: Check whether the file is empty" >> $log
        VFILECHECK=$(zcat Sdatadir/SvSrcFile | head -1)

        if [[ -z $VFILECHECK ]]; then
            stamp "The source file is empty." >> $log
            emptysrcfile
            Checkrc -r 99
        fi
    fi

    if JobStep "Section 2: Create work table for Exchange Partition"; then
        stamp "Section 2: Create work table for Exchange Partition" >> $log
        SqlExecute -u od_sec -t oracle -f $bindir/SvScript.create_tmp_dly_optns_quots.sql -l $log
    fi

    if JobStep "Section 3: Powermart to create insert file to load SvTgtTable"; then
        stamp "Section 3.1: Use OdControlMaxId for SvTgtTable and DLY_OPTNS_QUOTS_ID" >> $log
        ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID

        stamp "Section 3.2: Get current batch date for parm file" >> $log
        SqlExecute -t oracle -f $bindir/SvScript.get_date_parm_file.sql -l $log

        stamp "Section 3.3: Create parameter file and pass PROC_DT" >> $log
        cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

        stamp "Section 3.4: Calling the powermart session to create insert file from the source file" >> $log
        Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 -l $log
    fi

    if JobStep "Section 4: Execute exchange partition of TMP_DLY_OPTNS_QUOTS with SvTgtTable"; then
        stamp "Section 4: Execute exchange partition" >> $log
        db_chunk_size
        SqlExecute -u od_sec -t oracle -f $bindir/SvScript.exchange_partition.sql -l $log
    fi

    if JobStep "Section 5: Drop Temporary work table TMP_DLY_OPTNS_QUOTS"; then
        stamp "Section 5: Drop Temporary work table TMP_DLY_OPTNS_QUOTS" >> $log
        # Drop table command here
    fi

    if JobStep "Section 6: Run stats on SvTgtTable"; then
        stamp "Section 6: Run stats on $vTgtTable" >> $log
        db_chunk_size

    fi

    if JobStep "Section 7: Purge data older than 7 days"; then
        stamp "Section 7: Purge data older than 7 days" >> $log
        PurgeIntervalPartitions -u od_sec -t $vTgtTable -l $log
    fi
}

function emptysrcfile {
    stamp "Send e-mail to notify source file is empty" >> $log
    rm -f Stmpdir/SvScript.email

    stamp "Creating 'To' list for email" >> $log
    recipients=$(awk '/d/ {print $0}' Scontrol/muscript/SAPP_ENV.email.cfg)
    subject="$APP_ENV : $vSrcFile received is empty"

    echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients"
    Checkrc -r $?
    getfilebypass
    return 0
}

MainProcess
exit 0
SAPP_ENV' : 'SvSrcFile' received is empty'
"SvSrcFile received
date +%Y-%m-%d
cat Stmpdir/Svscript. email| mail-s "Svsubject" "e Recipients empty" » Stmpdir/SvScript. email
Checkrc -r $? 
return 0
}
MainProcess
Finalize
Exit 0