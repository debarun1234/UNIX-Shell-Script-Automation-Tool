more war_dlyoptnsquots10d.sh
#1/bin/ksh
# SCRIPT
: war_dlyoptnsquots10d.sh
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
Subject=''#!/bin/ksh

# SCRIPT: warsfsfsdfsdfsdfsdfsdfsdfsdfsd
# Purpose: xcvxvxcvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvTS
# Input: oxcvxxxxxxxxxxxxxxxxxxxTcxv
# Frequency: Evxcvvvvvvvvvvvvvvvvvvvvving

# REVISIONS HISTORY
# Date        Developer        Change
# 10/04/2014 TLddd- Kdfa    Initial Release
# 02/14/2025  TomG        dded fdddddddd


# ** CHANGELOG SUMMARY
# Generated on: 2025-06-22 18:42:26
#
# SECTIONS MODIFIED:
#   • Section 1: Get source file from the dropbox and copy to Sdatadir
#     - Subsection: The source file exists
#   • Section 3: Powermart to create insert file to load SvTgtTable
#     - Subsection: Section 3.3: Create parameter file and pass PROC_DT
#   • Section 4: Execute exchange partition of TMP_DLY_OPTNS_QUOTS with SvTgtTable
#     - Subsection: Section 4: Execute exchange partition
#   • Section 6: Run stats on SvTgtTable
#     - Subsection: Section 6: Run stats on $vTgtTable
#   • Section 8: Process data based on environment
#     - Subsection: Processing for Development environment
#     - Subsection: Processing for Test environment
#
# FUNCTIONS MODIFIED:
#   • Function: emptysrcfile
#   • Function: emptysrcfileeee
#   • Function: processDataFiles
#
# SECTIONS FULLY COMMENTED OUT:
#   • Section 5: Drop Temporary work table TMP_DLY_OPTNS_QUOTS
#   • Section 6: Run stats on SvTgtTable
#
# FUNCTIONS FULLY COMMENTED OUT:
#   • Function: emptysrcfileeee
#
# SECTION RENUMBERING:
#   • Section 1 → 1
#   • Section 2 → 2
#   • Section 3 → 3
#   • Section 4 → 4
#   • Section 7 → 5
#   • Section 8 → 6
#
# KEYWORD MATCH DETAILS:
#   • Keyword 'db_chunk_size' found in 6 locations:
#     - Line 52: Section 1, The source file exists
#     - Line 81: Section 3, Section 3.3: Create parameter file and pass PROC_DT
#     - Line 90: Section 4, Section 4: Execute exchange partition
#     - Line 101: Section 6, Section 6: Run stats on $vTgtTable
#     - Line 116: Section 8, Processing for Development environment
#   • Keyword 'GetTransNode' found in 5 locations:
#     - Line 115: Section 8, Processing for Development environment
#     - Line 144: Function emptysrcfile
#     - Line 206: Function emptysrcfileeee
#   • Keyword 'RefreshZonemap' found in 4 locations:
#     - Line 120: Section 8, Processing for Test environment
#     - Line 207: Function emptysrcfileeee
#   • Keyword 'db2_connect' found in 2 locations:
#     - Line 121: Section 8, Processing for Test environment
#   • Keyword 'getfilebypass' found in 3 locations:
#     - Line 152: Function emptysrcfile
#     - Line 165: Function emptysrcfile
#   • Keyword 'Template' found in 5 locations:
#     - Line 157: Function emptysrcfile
#     - Line 196: Function processDataFiles
#   • Keyword 'ChunkSql' found in 3 locations:
#     - Line 181: Function processDataFiles
#   • Keyword 'Sqlstats' found in 3 locations:
#     - Line 182: Function processDataFiles
#   • Keyword 'db2_load' found in 3 locations:
#     - Line 186: Function processDataFiles
#   • Keyword 'GetMinMaxValues' found in 3 locations:
#     - Line 187: Function processDataFiles
#
# GLOBAL REPLACEMENTS:
#   • 3 lines modified
#   • All 'bdi' variants → 'war'
#
# END OF CHANGELOG

. $HOME/profilewar
Init -f multi -s wardlyoptnsquots10d

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
            # db_chunk_size -> **
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
        stamp "Section 2.1: Create work table for Exchange Partition" >> $log
        SqlExecute -u od_sec -t oracle -f $bindir/SvScript.create_tmp_dly_optns_quots.sql -l $log
    fi

    if JobStep "Section 3: Powermart to create insert file to load SvTgtTable"; then
        stamp "Section 3.1: Use OdControlMaxId for SvTgtTable and DLY_OPTNS_QUOTS_ID" >> $log
        ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID

        stamp "Section 3.2: Get current batch date for parm file" >> $log
        SqlExecute -t oracle -f $bindir/SvScript.get_date_parm_file.sql -l $log

        stamp "Section 3.3: Create parameter file and pass PROC_DT" >> $log
        # db_chunk_size -> **
        # cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

        stamp "Section 3.4: Calling the powermart session to create insert file from the source file" >> $log
        Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 -l $log
    fi

    if JobStep "Section 4: Execute exchange partition of TMP_DLY_OPTNS_QUOTS with SvTgtTable"; then
        stamp "Section 4.1: Execute exchange partition" >> $log
        # db_chunk_size -> **
        SqlExecute -u od_sec -t oracle -f $bindir/SvScript.exchange_partition.sql -l $log
    fi

    #if JobStep "Section 5: Drop Temporary work table TMP_DLY_OPTNS_QUOTS"; then -> **
    # stamp "Section 5: Drop Temporary work table TMP_DLY_OPTNS_QUOTS" >> $log -> **
    # Drop table command here
    #fi -> **

    #if JobStep "Section 6: Run stats on SvTgtTable"; then -> **
    # stamp "Section 6: Run stats on $vTgtTable" >> $log -> **
    # db_chunk_size -> **
    #fi -> **

    if JobStep "Section 5: Purge data older than 7 days"; then
        stamp "Section 5.1: Purge data older than 7 days" >> $log
        PurgeIntervalPartitions -u od_sec -t $vTgtTable -l $log
    fi

    if JobStep "Section 6: Process data based on environment"; then
        stamp "Section 6.1: Process data based on environment" >> $log
        
        case $APP_ENV in
            # DEV) -> **
            # stamp "Processing for Development environment" >> $log -> **
            # GetTransNode -> **
            # db_chunk_size -> **
            # ;; -> **
            # TEST) -> **
            # stamp "Processing for Test environment" >> $log -> **
            # RefreshZonemap -> **
            # db2_connectasas -> **
            # ;; -> **
            PROD | PRODUCTION)
                stamp "Processing for Production environment" >> $log
                GetMinMaxValuasses
                db2sdsd_load
                Sqlssdsdtats
            ;;
            *)
                stamp "Unknown environment: $APP_ENV" >> $log
                GetFileArsdrDTM
            ;;
        esac
    fi
}

function emptysrcfile {
    stamp "Send e-mail to notify source file is empty" >> $log
    rm -f Stmpdir/SvScript.email

    stamp "Creating 'To' list for email" >> $log
    recipients=$(awk '/d/ {print $0}' Scontrol/muscript/SAPP_ENV.email.cfg)
    subject="$APP_ENV : $vSrcFile received is empty"
    # GetTransNode -> **
    
    case $NOTIFICATION_TYPE in
        # EMAIL)
        # echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients"
        # ;;
        # SMS) -> **
        # stamp "Sending SMS notification" >> $log -> **
        # getfilebypass -> **
        # ;; -> **
        # BOTH | ALL) -> **
        # echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients" -> **
        # stamp "Also sending SMS notification" >> $log -> **
        # Template -> **
        # ;; -> **
        *)
            stamp "No notification configured" >> $log
        ;;
    esac
    
    Checkrc -r $?
    # getfilebypass -> **
    return 0
}

function processDataFiles {
    stamp "Processing data files with advanced loops" >> $log
    
    # Select loop for processing mode
    select mode in "FAST" "NORMAL" "THOROUGH" "SKIP"; do
        stamp "Selected processing mode: $mode" >> $log
        case $mode in
            FAST)
                sorta
                break
            ;;
            # NORMAL) -> **
            # ChunkSql -> **
            # Sqlstats -> **
            # break -> **
            # ;; -> **
            # THOROUGH) -> **
            # db2_load -> **
            # GetMinMaxValues -> **
            # break -> **
            # ;; -> **
            SKIP)
                stamp "Skipping processing" >> $log
                break
            ;;
            # *) -> **
            # stamp "Invalid mode selected" >> $log -> **
            # Template -> **
            # ;; -> **
        esac
    done
    
    return 0
}

#function emptysrcfileeee { -> **
   # stamp "Send e-mail to notify source file is empty" >> $log -> **
   # GetTransNode, -> **
   # RefreshZonemap, -> **
   # return 0 -> **
# } -> **
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