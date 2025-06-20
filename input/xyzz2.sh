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

# SCRIPT: bdi_dlyoptnsquots10d.sh
# Purpose: Loads data from flat file omdd.quotes.gz to OD_SEC table, DLY_OPTNS_QUOTS
# Input: omdd.quotes.gz
# Output: OD_SEC.DLY_OPTNS_QUOTS
# Frequency: Event-based scheduling

# REVISIONS HISTORY
# Date        Developer        Change
# 10/04/2017  TL- Kim Evens    Initial Release
# 02/14/2023  Vijetha G        Added failure check to section 1.2 (BCPJ-3111)


# CHANGELOG SUMMARY WILL BE CREATED HERE below


###############################################################

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

    # Sample input Josbstep form
    if JobStep "Section 2: Create work table for Exchange Partition"; then
        stamp "Section 2: Create work table for Exchange Partition" >> $log
        SqlExecute -u od_sec -t oracle -f $bindir/SvScript.create_tmp_dly_optns_quots.sql -l $log
    fi

    #Sample output JobStep form here if we see the all the lines are commnented then stamp and JobStep will be commented out and next section will be renumbered.
    # if JobStep "Section 2: Create work table for Exchange Partition"; then
    #     stamp "Section 2: Create work table for Exchange Partition" >> $log
            # db_chunk_size
            # SqlExecute -u od_sec -t oracle -f $bindir/SvScript.create_tmp_dly_optns_quots.sql -l $log

    # fi


    # Sample input JobStep form with Subsections
    if JobStep "Section 3: Powermart to create insert file to load SvTgtTable"; then
        stamp "Section 3.1: Use OdControlMaxId for SvTgtTable and DLY_OPTNS_QUOTS_ID" >> $log
        ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID
        db_chunk_size
        stamp "Section 3.2: Get current batch date for parm file" >> $log
        SqlExecute -t oracle -f $bindir/SvScript.get_date_parm_file.sql -l $log
        
        stamp "Section 3.3: Create parameter file and pass PROC_DT" >> $log
        cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

        stamp "Section 3.4: Calling the powermart session to create insert file from the source file" >> $log
        Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 -l $log
    fi

    #Sample output 1: JobStep form with Subsections - if any matched keywords are found and commented in any respective subsetiosn yet it has other uncommented lines then the enture section will be left untouche
        if JobStep "Section 3: Powermart to create insert file to load SvTgtTable"; then
        stamp "Section 3.1: Use OdControlMaxId for SvTgtTable and DLY_OPTNS_QUOTS_ID" >> $log
        ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID
        # db_chunk_size   
        stamp "Section 3.2: Get current batch date for parm file" >> $log
        SqlExecute -t oracle -f $bindir/SvScript.get_date_parm_file.sql -l $log
        
        stamp "Section 3.3: Create parameter file and pass PROC_DT" >> $log
        cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

        stamp "Section 3.4: Calling the powermart session to create insert file from the source file" >> $log
        Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 -l $log
    fi

    #Sample output 2: JobStep form with Subsections - if any subsetion has mutiple lines and either of 1 is commented due to kewords or precommented then that subsection starting with stamp wont be commented other it will be commented
        if JobStep "Section 3: Powermart to create insert file to load SvTgtTable"; then
        stamp "Section 3.1: Use OdControlMaxId for SvTgtTable and DLY_OPTNS_QUOTS_ID" >> $log
        ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID
        # db_chunk_size
        # stamp "Section 3.2: Get current batch date for parm file" >> $log
        # SqlExecute -t oracle -f $bindir/SvScript.get_date_parm_file.sql -l $log
        # GetTransNode
        stamp "Section 3.3: Create parameter file and pass PROC_DT" >> $log
        cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

        stamp "Section 3.4: Calling the powermart session to create insert file from the source file" >> $log
        Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 -l $log
    fi

    #Sample output 3: JobStep form with Subsections - if all the contents of each subesction is either found precommented or commented due to keywords then all the subsections will be commented out including the main jobstep section and the next jobstep section will be renumbered as usual.
        # if JobStep "Section 3: Powermart to create insert file to load SvTgtTable"; then
        # stamp "Section 3.1: Use OdControlMaxId for SvTgtTable and DLY_OPTNS_QUOTS_ID" >> $log
        # #ControlMaxid -d oracle -u od_sec -t $vTgtTable -c DLY_OPTNS_QUOTS_ID
        # db_chunk_size
        # stamp "Section 3.2: Get current batch date for parm file" >> $log
        # SqlExecute -t oracle -f $bindir/SvScript.get_date_parm_file.sql -l $log
        # GetTransNode
        # stamp "Section 3.3: Create parameter file and pass PROC_DT" >> $log
        # cat Sdatadir/SvScript.get_date_parm_file.txt >> Stmpdir/SvScript.param

        # stamp "Section 3.4: Calling the powermart session to create insert file from the source file" >> $log
        # Runworkflow -f UDM_STG -s wf_m_dly_optns_quots -e 1 -l $log
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
        stamp "Section 7: Purge data older than 7 days" >> $log    # this line is to be counted as a part of the entire jobstep header as the `stamp` function is used to log the job step
        PurgeIntervalPartitions -u od_sec -t $vTgtTable -l $log
    fi
}

# Sample Input function form
function emptysrcfile {
    stamp "Send e-mail to notify source file is empty" >> $log
    rm -f Stmpdir/SvScript.email

    stamp "Creating 'To' list for email" >> $log
    recipients=$(awk '/d/ {print $0}' Scontrol/muscript/SAPP_ENV.email.cfg)
    subject="$APP_ENV : $vSrcFile received is empty"
    GetTransNode
    echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients"
    Checkrc -r $?
    getfilebypass
    return 0
}

#Sample output function form (please note the changes made)
function emptysrcfile {
    stamp "Send e-mail to notify source file is empty" >> $log
    # rm -f Stmpdir/SvScript.email

    stamp "Creating 'To' list for email" >> $log
    recipients=$(awk '/d/ {print $0}' Scontrol/muscript/SAPP_ENV.email.cfg)
    subject="$APP_ENV : $vSrcFile received is empty"
    # GetTransNode
    echo "Source file $vSrcFile received on $(date +%Y-%m-%d) is empty" | mail -s "$subject" "$recipients"
    Checkrc -r $?
    # getfilebypass
    return 0
} # if you see some of the lines and the keywords specific to the keywowrds.txt are commented out. So the function stays as it is however the next sample output is little different.

# Sample output function form with slight changes if all the lines are commented out like the gettransnode and getfilebypass then entire fucntion will be commented out
# function emptysrcfileeee {
   #stamp "Send e-mail to notify source file is empty" >> $log
   # GetTransNode
   # RefreshZonemap
   # return 0
#}


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