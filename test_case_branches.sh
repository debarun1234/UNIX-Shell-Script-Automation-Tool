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


# CHANGELOG SUMMARY
# Generated on: 2025-06-20 22:49:23
#
# SECTIONS MODIFIED:
#   • Section 1: Get source file from the dropbox and copy to Sdatadir
#     - Subsection: The source file exists
#   • Section 4: Execute exchange partition of TMP_DLY_OPTNS_QUOTS with SvTgtTable
#     - Subsection: Section 4: Execute exchange partition
#   • Section 6: Run stats on SvTgtTable
#     - Subsection: Section 6: Run stats on $vTgtTable
#   • Section 8: Process data based on environment
#     - Subsection: Processing for Development environment
#     - Subsection: Processing for Test environment
#   • Section 9: Process files with loops
#     - Subsection: Processing iteration: $i
#     - Subsection: Processing file type: $file_type
#     - Subsection: Processing day: $day
#   • Section 10: Process with until and select loops
#     - Subsection: Retry attempt remaining: $retry_count
#     - Subsection: Waiting for completion flag
#     - Subsection: Selected Development environment
#     - Subsection: Selected Test environment
#     - Subsection: Selected Production environment
#     - Subsection: Invalid selection: $REPLY
#     - Subsection: Processing file type: $file_type
#     - Subsection: Processing all file types
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
#   • Section 9 → 7
#   • Section 10 → 8
#
# KEYWORD MATCH DETAILS:
#   • Keyword 'db_chunk_size' found in 9 locations:
#     - Line 52: Section 1, The source file exists
#     - Line 89: Section 4, Section 4: Execute exchange partition
#     - Line 100: Section 6, Section 6: Run stats on $vTgtTable
#     - Line 116: Section 8, Processing for Development environment
#     - Line 143: Section 9, Processing iteration: $i
#     - Line 170: Section 10, Retry attempt remaining: $retry_count
#   • Keyword 'GetTransNode' found in 14 locations:
#     - Line 115: Section 8, Processing for Development environment
#     - Line 142: Section 9, Processing iteration: $i
#     - Line 169: Section 10, Retry attempt remaining: $retry_count
#     - Line 247: Function emptysrcfile
#     - Line 368: Function emptysrcfileeee
#   • Keyword 'RefreshZonemap' found in 12 locations:
#     - Line 120: Section 8, Processing for Test environment
#     - Line 157: Section 9, Processing day: $day
#     - Line 187: Section 10, Selected Development environment
#     - Line 369: Function emptysrcfileeee
#   • Keyword 'db2_connect' found in 6 locations:
#     - Line 121: Section 8, Processing for Test environment
#     - Line 221: Section 10, Processing file type: $file_type
#   • Keyword 'Template' found in 27 locations:
#     - Line 149: Section 9, Processing file type: $file_type
#     - Line 177: Section 10, Waiting for completion flag
#     - Line 225: Section 10, Processing file type: $file_type
#     - Line 260: Function emptysrcfile
#     - Line 305: Function processDataFiles
#     - Line 330: Function processDataFiles
#     - Line 358: Function processDataFiles
#   • Keyword 'Sort' found in 12 locations:
#     - Line 150: Section 9, Processing file type: $file_type
#     - Line 178: Section 10, Waiting for completion flag
#     - Line 229: Section 10, Processing all file types
#     - Line 312: Function processDataFiles
#   • Keyword 'ChunkSql' found in 15 locations:
#     - Line 151: Section 9, Processing file type: $file_type
#     - Line 192: Section 10, Selected Test environment
#     - Line 320: Function processDataFiles
#     - Line 343: Function processDataFiles
#   • Keyword 'db2_sql' found in 6 locations:
#     - Line 158: Section 9, Processing day: $day
#     - Line 218: Section 10, Processing file type: $file_type
#   • Keyword 'GetMinMaxValues' found in 13 locations:
#     - Line 197: Section 10, Selected Production environment
#     - Line 270: Function emptysrcfile
#     - Line 349: Function processDataFiles
#   • Keyword 'db2_load' found in 13 locations:
#     - Line 198: Section 10, Selected Production environment
#     - Line 313: Function processDataFiles
#     - Line 348: Function processDataFiles
#   • Keyword 'GetFileArrDTM' found in 12 locations:
#     - Line 207: Section 10, Invalid selection: $REPLY
#     - Line 304: Function processDataFiles
#     - Line 329: Function processDataFiles
#   • Keyword 'Sqlstats' found in 14 locations:
#     - Line 217: Section 10, Processing file type: $file_type
#     - Line 321: Function processDataFiles
#     - Line 344: Function processDataFiles
#   • Keyword 'db2_disconnect' found in 12 locations:
#     - Line 222: Section 10, Processing file type: $file_type
#     - Line 280: Function emptysrcfile
#     - Line 288: Function emptysrcfile
#   • Keyword 'getfilebypass' found in 11 locations:
#     - Line 255: Function emptysrcfile
#     - Line 287: Function emptysrcfile
#     - Line 293: Function emptysrcfile
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
        cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

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
            DEV)
                stamp "Processing for Development environment" >> $log
            # GetTransNode -> **
            # db_chunk_size -> **
            ;;
            TEST)
                stamp "Processing for Test environment" >> $log
            # RefreshZonemap -> **
            # db2_connectasas -> **
            ;;
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

    if JobStep "Section 7: Process files with loops"; then
        stamp "Section 7.1: Process files with loops" >> $log
        
        # C-style for loop (restricted)
        for (( i=0; i<5; i++ )); do
            stamp "Processing iteration: $i" >> $log
            # GetTransNode -> **
            # db_chunk_size -> **
        done
        
        # List-based for loop (unrestricted)
        for file_type in "quotes" "trades" "orders"; do
            stamp "Processing file type: $file_type" >> $log
            # Template -> **
            # Sort -> **
            # ChunkSql -> **
        done
        
        # Range-based for loop
        for day in {1..7}; do
            stamp "Processing day: $day" >> $log
            # RefreshZonemap -> **
            # db2_sql -> **
        done
    fi

    if JobStep "Section 8: Process with until and select loops"; then
        stamp "Section 8.1: Process with until and select loops" >> $log
        
        # Until loop with numeric condition
        retry_count=5
        until [ $retry_count -eq 0 ]; do
            stamp "Retry attempt remaining: $retry_count" >> $log
            # GetTransNode -> **
            # db_chunk_size -> **
            retry_count=$((retry_count - 1))
        done
        
        # Until loop with file check (unrestricted)
        until [ -f "$COMPLETED_FLAG" ]; do
            stamp "Waiting for completion flag" >> $log
            # Template -> **
            # Sort -> **
            sleep 30
        done
        
        # Select loop for environment selection
        select environment in "DEV" "TEST" "PROD" "EXIT"; do
            case $environment in
                DEV)
                    stamp "Selected Development environment" >> $log
                # RefreshZonemap -> **
                    break
                ;;
                TEST)
                    stamp "Selected Test environment" >> $log
                # ChunkSql -> **
                    break
                ;;
                PROD)
                    stamp "Selected Production environment" >> $log
                # GetMinMaxValues -> **
                # db2_load -> **
                    break
                ;;
                EXIT)
                    stamp "Exiting selection" >> $log
                    break
                ;;
                *)
                    stamp "Invalid selection: $REPLY" >> $log
                # GetFileArrDTM -> **
                ;;
            esac
        done
        
        # Select loop for file types (unrestricted)
        select file_type in quotes trades orders summary all; do
            stamp "Processing file type: $file_type" >> $log
            case $file_type in
                quotes)
                # Sqlstats -> **
                # db2_sql -> **
                ;;
                trades | orders)
                # db2_connect -> **
                # db2_disconnect -> **
                ;;
                summary)
                # Template -> **
                ;;
                all)
                    stamp "Processing all file types" >> $log
                # Sort -> **
                    break
                ;;
                *)
                    stamp "Unknown file type selected" >> $log
                ;;
            esac
        done
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
        EMAIL)
            echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients"
        ;;
        SMS)
            stamp "Sending SMS notification" >> $log
        # getfilebypass -> **
        ;;
        BOTH | ALL)
            echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients"
            stamp "Also sending SMS notification" >> $log
        # Template -> **
        ;;
        *)
            stamp "No notification configured" >> $log
        ;;
    esac
    
    # Loop through retry attempts
    for (( attempt=1; attempt<=3; attempt++ )); do
        stamp "Notification attempt: $attempt" >> $log
        # GetMinMaxValues -> **
        if [[ $? -eq 0 ]]; then
            break
        fi
    done
    
    # Process different notification channels
    for channel in "primary" "secondary" "backup"; do
        stamp "Checking $channel notification channel" >> $log
        getfilebyepass
        # db2_disconnect -> **
    done
    
    # Until loop for connection retry
    connection_attempts=0
    until [ $connection_attempts -ge 5 ] || [ "$CONNECTION_STATUS" = "SUCCESS" ]; do
        stamp "Database connection attempt: $((connection_attempts + 1))" >> $log
        # getfilebypass -> **
        # db2_disconnect -> **
        connection_attempts=$((connection_attempts + 1))
    done
    
    Checkrc -r $?
    # getfilebypass -> **
    return 0
}

function processDataFiles {
    stamp "Processing data files with advanced loops" >> $log
    
    # Array-based for loop
    declare -a file_extensions=("gz" "txt" "csv" "dat")
    for ext in "${file_extensions[@]}"; do
        stamp "Processing .$ext files" >> $log
        # GetFileArrDTM -> **
        # Template -> **
    done
    
    # While loop with counter
    counter=0
    while [[ $counter -lt 10 ]]; do
        stamp "Processing batch: $counter" >> $log
        # Sorte -> **
        # db2_load -> **
        ((counter++))
    done
    
    # While loop reading from file
    while IFS= read -r line; do
        stamp "Processing line: $line" >> $log
        # ChunkSql -> **
        # Sqlstats -> **
        done < "$datafile"
    
        # Until loop for data processing completion
        processed_files=0
        total_files=100
    until [ $processed_files -ge $total_files ]; do
        stamp "Processed $processed_files of $total_files files" >> $log
        # GetFileArrDTM -> **
        # Template -> **
        processed_files=$((processed_files + 10))
    done
    
        # Select loop for processing mode
    select mode in "FAST" "NORMAL" "THOROUGH" "SKIP"; do
        stamp "Selected processing mode: $mode" >> $log
        case $mode in
            FAST)
                sorta
                break
            ;;
            NORMAL)
            # ChunkSql -> **
            # Sqlstats -> **
                break
            ;;
            THOROUGH)
            # db2_load -> **
            # GetMinMaxValues -> **
                break
            ;;
            SKIP)
                stamp "Skipping processing" >> $log
                break
            ;;
            *)
                stamp "Invalid mode selected" >> $log
            # Template -> **
            ;;
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