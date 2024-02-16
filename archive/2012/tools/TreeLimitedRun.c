//---------------------------------------------------------------------------
//----Program to watch CPU usage of a process
//----TreeLimitedRun <CPU time limit> <WC time limit> <Memory limit> <Job>
//---------------------------------------------------------------------------
//----SUN or LINUX
#define LINUX
//---------------------------------------------------------------------------
#include <stdio.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <stdlib.h>
#include <unistd.h>
#include <dirent.h>
#include <ctype.h>
#include <signal.h>
#ifdef SUN
#include <procfs.h>
#endif
//---------------------------------------------------------------------------
#define STRING_LENGTH 80
#define MAX_PROCESSES 1000
#define DEFAULT_DELAY_BETWEEN_CHECKS 10
#define NANOSECONDS 1E9
#define MICROSECONDS 1E6
#define JIFFIES 100

#define STDOUT 1
#define STDERR 2

typedef char String[STRING_LENGTH];

typedef struct {
    pid_t PID;
    pid_t PPID;
    long CPUTime;
    } ProcessData;
typedef ProcessData ProcessDataArray[MAX_PROCESSES];

typedef pid_t PIDArray[MAX_PROCESSES];

float WallClockSoFar(struct timeval WCStartTime);

float WCTimeChild = 0.0;
struct timeval WCStartTime;

int GlobalInterrupted;
int GlobalSignalReceived;
//---------------------------------------------------------------------------
void SIGCHLDHandler(int TheSignal) {

    int PID;
    int Status;

    PID = wait(&Status);
    WCTimeChild = WallClockSoFar(WCStartTime);
//DEBUG printf("The child %d has died\n",PID);
}
//---------------------------------------------------------------------------
//----Controllers in the CASC/SystemOnTPTP/SSCPA/etc hierarchy may send
//----SIGQUIT to stop things
void SIGQUITHandler(int TheSignal) {

//DEBUG printf("TreeLimitedRun %d got a signal %d\n",getpid(),TheSignal);
    GlobalInterrupted = 1;
    GlobalSignalReceived = TheSignal;

}
//---------------------------------------------------------------------------
void SetMemoryLimit(rlim_t MemoryLimit) {

    struct rlimit ResourceLimits;

//----Limit the memory. Need to get old one for hard limit field
    /*if (getrlimit(RLIMIT_AS,&ResourceLimits) == -1) {
        perror("TimeLimitedRun - Getting resource limit:");
        exit(-1);
    }*/
//----Set new memory limit
    ResourceLimits.rlim_max = MemoryLimit;
    ResourceLimits.rlim_cur = MemoryLimit; //---- -1 because its weird
    if (setrlimit(RLIMIT_AS,&ResourceLimits) == -1) {
        perror("TimeLimitedRun - Setting resource limit:");
        exit(-1);
    }
}
//---------------------------------------------------------------------------
//----Prevent core dumps that occur on timeout
void SetNoCoreDump(void) {

    struct rlimit ResourceLimits;

//----Get old resource limits
    if (getrlimit(RLIMIT_CORE,&ResourceLimits) == -1) {
        perror("CPULimitedRun - Getting resource limit:");
    }
//----Set new core limit to 0
    ResourceLimits.rlim_cur = 0;
    if (setrlimit(RLIMIT_CORE,&ResourceLimits) == -1) {
        perror("CPULimitedRun - Setting resource limit:");
    }
}
//---------------------------------------------------------------------------
#ifdef LINUX
void GetProcessesOwnedByMe(uid_t MyRealUID,ProcessDataArray OwnedPIDs,
int *NumberOfOwnedPIDs) {

    DIR *ProcDir;
    struct dirent *ProcessDir;
    pid_t UID,PID,PPID;
    FILE *ProcFile;
    String ProcFileName,Line;

    if ((ProcDir = opendir("/proc")) == NULL) {
        perror("ERROR: Cannot opendir /proc\n");
        exit(-1);
    }

//DEBUG printf("look for processes owned by %d\n",MyRealUID);

    *NumberOfOwnedPIDs = 0;
    while ((ProcessDir = readdir(ProcDir)) != NULL) {
        if (isdigit(ProcessDir->d_name[0])) {
            PID = (pid_t)atoi(ProcessDir->d_name);
            sprintf(ProcFileName,"/proc/%d/status",PID);
            if ((ProcFile = fopen(ProcFileName,"r")) != NULL) {
                PPID = -1;
                UID = -1;
                while ((PPID == -1 || UID == -1) &&
fgets(Line,STRING_LENGTH,ProcFile) != NULL) {
                    sscanf(Line,"PPid: %d",&PPID);
                    sscanf(Line,"Uid: %d",&UID);
                }
                fclose(ProcFile);
//----Check that data was found
//DEBUG printf("PID = %d PPID = %d UID = %d\n",PID,PPID,UID);
                if (PPID == -1 || UID == -1) {
                    fprintf(stderr,"Could not get process information\n");
                    exit(-1);
                }
//----Check if this process is owned by this user
                if (UID == MyRealUID) {
//----Record the PIDs as potentially relevant
                    OwnedPIDs[*NumberOfOwnedPIDs].PID = PID;
                    OwnedPIDs[*NumberOfOwnedPIDs].PPID = PPID;
                    (*NumberOfOwnedPIDs)++;
//DEBUG printf("%d I own PID = %d PPID = %d UID = %d\n",*NumberOfOwnedPIDs,PID,PPID,UID);
                    if (*NumberOfOwnedPIDs >= MAX_PROCESSES) {
                        fprintf(stderr,"ERROR: Out of save process space\n");
                        exit(-1);
                    }
                }
            } else {
//----Bloody child just died
            }
        }
    }
    closedir(ProcDir);
}
//---------------------------------------------------------------------------
float GetProcessTime(pid_t PID,int IncludeSelf,int IncludeChildren) {

    FILE *ProcFile;
    String ProcFileName;
    float MyTime,ChildTime,ProcessTime;
    int UserModeJiffies,SystemModeJiffies,ChildUserModeJiffies,
ChildSystemModeJiffies;

    ProcessTime = 0;
    sprintf(ProcFileName,"/proc/%d/stat",PID);
    if ((ProcFile = fopen(ProcFileName,"r")) != NULL) {
        fscanf(ProcFile,"%*d %*s %*c %*d %*d %*d %*d %*d %*u %*u %*u %*u %*u %d %d %d %d",&UserModeJiffies,&SystemModeJiffies,&ChildUserModeJiffies,
&ChildSystemModeJiffies);
        fclose(ProcFile);
//DEBUG printf("%d: my jiffies = %d, dead child jiffies = %d\n",PID,UserModeJiffies+SystemModeJiffies,ChildUserModeJiffies+ChildSystemModeJiffies);
//----Time used by this process
        MyTime = ((float)(UserModeJiffies + SystemModeJiffies))/JIFFIES;
//----Time used by this process's dead children (man pages are wrong - does
//----not include my jiffies)
        ChildTime = ((float)(ChildUserModeJiffies + ChildSystemModeJiffies))/
JIFFIES;
        if (IncludeSelf) {
            ProcessTime += MyTime;
        }
        if (IncludeChildren) {
            ProcessTime += ChildTime;
        }
        return(ProcessTime);
    } else {
//----Bloody child died, return 0 and catch it in the parent next time
        return(0);
    }
}
unsigned long GetProcessMem(pid_t PID) {

    FILE *ProcFile;
    String ProcFileName;
    unsigned long vsize;

    sprintf(ProcFileName,"/proc/%d/stat",PID);
    if ((ProcFile = fopen(ProcFileName,"r")) != NULL) {
        fscanf(ProcFile,"%*d %*s %*c %*d %*d %*d %*d %*d %*u %*u %*u %*u %*u %*d %*d %*d %*d %*ld %*ld %*ld %*ld %*lu %lu",&vsize);
        fclose(ProcFile);
        return(vsize);
    } else {
        return(0);
    }
}
#endif
//---------------------------------------------------------------------------
#ifdef SUN
void GetProcessesOwnedByMe(uid_t MyRealUID,ProcessDataArray OwnedPIDs,
int *NumberOfOwnedPIDs) {

    DIR *ProcDir;
    struct dirent *ProcessDir;
    pid_t PID;
    struct psinfo ProcessRecord;
    FILE *ProcFile;
    String ProcFileName;

    if ((ProcDir = opendir("/proc")) == NULL) {
        perror("ERROR: Cannot opendir /proc\n");
        exit(-1);
    }

//DEBUG printf("look for processes owned by %d\n",MyRealUID);

    *NumberOfOwnedPIDs = 0;
    while ((ProcessDir = readdir(ProcDir)) != NULL) {
        if (isdigit((int)ProcessDir->d_name[0])) {
            PID = (pid_t)atoi(ProcessDir->d_name);
            sprintf(ProcFileName,"/proc/%d/psinfo",(int)PID);
            if ((ProcFile = fopen(ProcFileName,"r")) != NULL) {
                fread(&ProcessRecord,sizeof(ProcessRecord),1,ProcFile);
                fclose(ProcFile);
//----Check if this process is owned by this user
                if (ProcessRecord.pr_uid == MyRealUID) {
//----Record the PIDs as potentially relevant
                    OwnedPIDs[*NumberOfOwnedPIDs].PID = PID;
                    OwnedPIDs[*NumberOfOwnedPIDs].PPID = ProcessRecord.pr_ppid;
                    (*NumberOfOwnedPIDs)++;
                    if (*NumberOfOwnedPIDs >= MAX_PROCESSES) {
                        fprintf(stderr,"ERROR: Out of save process space\n");
                        exit(-1);
                    }
                }
            } else {
//----Bloody child just died
            }
        }
    }
    closedir(ProcDir);
}
//---------------------------------------------------------------------------
float GetProcessTime(pid_t PID,int IncludeSelf,int IncludeChildren) {

    FILE *ProcFile;
    String ProcFileName;
    pstatus_t StatusRecord;
    float ProcessTime;

    ProcessTime = 0;
    sprintf(ProcFileName,"/proc/%d/status",(int)PID);
    if ((ProcFile = fopen(ProcFileName,"r")) != NULL) {
        fread(&StatusRecord,sizeof(StatusRecord),1,ProcFile);
        fclose(ProcFile);
        if (IncludeSelf) {
            ProcessTime += StatusRecord.pr_utime.tv_sec +
StatusRecord.pr_stime.tv_sec +
((float)(StatusRecord.pr_utime.tv_nsec+StatusRecord.pr_stime.tv_nsec))/
NANOSECONDS;
        }
        if (IncludeChildren) {
            ProcessTime += StatusRecord.pr_cutime.tv_sec +
StatusRecord.pr_cstime.tv_sec +
((float)(StatusRecord.pr_cutime.tv_nsec+StatusRecord.pr_cstime.tv_nsec))/
NANOSECONDS;
        }
//DEBUG printf("Process %d has used U %ld +n%ld + S %ld +n%ld + CU %ld +n%ld + CS %ld +n%ld = %.1f\n",
//DEBUG PID,StatusRecord.pr_utime.tv_sec,StatusRecord.pr_utime.tv_nsec,
//DEBUG StatusRecord.pr_stime.tv_sec,StatusRecord.pr_stime.tv_nsec,
//DEBUG StatusRecord.pr_cutime.tv_sec,StatusRecord.pr_cutime.tv_nsec,
//DEBUG StatusRecord.pr_cstime.tv_sec,StatusRecord.pr_cstime.tv_nsec,
//DEBUG ProcessTime);
        return(ProcessTime);
    } else {
//----Bloody child died, return 0 and catch it in the parent next time
        return(0);
    }
}
#endif //----SUN
//---------------------------------------------------------------------------
int PIDInArray(pid_t PID,ProcessDataArray PIDs,int NumberOfPIDs) {

    int PIDIndex;

    for (PIDIndex = 0;PIDIndex < NumberOfPIDs;PIDIndex++) {
        if (PIDs[PIDIndex].PID == PID) {
            return(1);
        }
    }
    return(0);
}
//---------------------------------------------------------------------------
int ExtractTree(pid_t FirstBornPID,ProcessDataArray OwnedPIDs,
int NumberOfOwnedPIDs,PIDArray TreePIDs) {

    int NumberOfTreePIDs;
    int CurrentTreeIndex;
    int OwnedIndex;

//----Find those in the process tree, and get their times
    CurrentTreeIndex = 0;
    TreePIDs[CurrentTreeIndex] = FirstBornPID;
    NumberOfTreePIDs = 1;

    while (CurrentTreeIndex < NumberOfTreePIDs) {
//DEBUG printf("%d is in the tree\n",TreePIDs[CurrentTreeIndex]);
//----Keep scanning for offspring until tree ends
        for (OwnedIndex = 0; OwnedIndex < NumberOfOwnedPIDs; OwnedIndex++) {
            if (OwnedPIDs[OwnedIndex].PPID == TreePIDs[CurrentTreeIndex]) {
                TreePIDs[NumberOfTreePIDs++] = OwnedPIDs[OwnedIndex].PID;
            }
        }
//----Move on to the next process in the tree
        CurrentTreeIndex++;
    }

    return(NumberOfTreePIDs);
}
//---------------------------------------------------------------------------
int GetTreePIDs(uid_t MyRealUID,pid_t FirstBornPID,PIDArray TreePIDs) {

    ProcessDataArray OwnedPIDs;
    int NumberOfOwnedPIDs;
    int NumberOfTreePIDs;

//----Get the list of processes owned by this user
    GetProcessesOwnedByMe(MyRealUID,OwnedPIDs,&NumberOfOwnedPIDs);

//----Check that the root of the tree is still there
//DEBUG printf("Check if %d is alive\n",FirstBornPID);
    if (!PIDInArray(FirstBornPID,OwnedPIDs,NumberOfOwnedPIDs)) {
//DEBUG printf("It is dead\n");
        return(0);
    }
//DEBUG printf("It is alive\n");

    NumberOfTreePIDs = ExtractTree(FirstBornPID,OwnedPIDs,NumberOfOwnedPIDs,
TreePIDs);

    return(NumberOfTreePIDs);
}
//---------------------------------------------------------------------------
int KillTree(uid_t MyRealUID,pid_t FirstBornPID,int Signal) {

    PIDArray TreePIDs;
    int Index;
    int NumberOfTreePIDs;

    NumberOfTreePIDs = GetTreePIDs(MyRealUID,FirstBornPID,TreePIDs);

//----Kill gently, then viciously. Important, the first born gets it first
//----so that it can curb its descendants nicely
    for (Index=0;Index < NumberOfTreePIDs;Index++) {
        kill(TreePIDs[Index],Signal);
//----Give top process time to tidy up offspring
        if (Index == 0) {
            sleep(1);
        }
    }
    sleep(1);
    for (Index=0;Index < NumberOfTreePIDs;Index++) {
//DEBUG printf("Kill PID %d with SIGKILL\n",TreePIDs[Index]);
        kill(TreePIDs[Index],SIGKILL);
    }

    return(NumberOfTreePIDs);
}
//---------------------------------------------------------------------------
int KillOrphans(uid_t MyRealUID,ProcessDataArray SavePIDs,
int NumberOfSavePIDs) {

    ProcessDataArray OwnedPIDs;
    int NumberOfOwnedPIDs;
    int OwnedIndex;
    int NumberOfOrphansKilled;

//----Get the list of processes owned by this user
    GetProcessesOwnedByMe(MyRealUID,OwnedPIDs,&NumberOfOwnedPIDs);

    NumberOfOrphansKilled = 0;
    for (OwnedIndex = 0; OwnedIndex < NumberOfOwnedPIDs; OwnedIndex++) {
//DEBUG printf("!!! Consider %d with parent %d\n",OwnedPIDs[OwnedIndex].PID, OwnedPIDs[OwnedIndex].PPID);
        if (OwnedPIDs[OwnedIndex].PPID == 1 &&
!PIDInArray(OwnedPIDs[OwnedIndex].PID,SavePIDs,NumberOfSavePIDs)) {
//DEBUG printf("!!!Kill orphaned tree with root %d\n",OwnedPIDs[OwnedIndex].PID);
            NumberOfOrphansKilled += KillTree(MyRealUID,
OwnedPIDs[OwnedIndex].PID,0);
        }
    }
    return(NumberOfOrphansKilled);
}
//---------------------------------------------------------------------------
int TimeTree(uid_t MyRealUID,pid_t FirstBornPID,float *TreeTime) {

    PIDArray TreePIDs;
    int NumberOfTreePIDs;
    int Index;

    *TreeTime = 0;

    NumberOfTreePIDs = GetTreePIDs(MyRealUID,FirstBornPID,TreePIDs);

    for (Index=0;Index < NumberOfTreePIDs;Index++) {
        *TreeTime += GetProcessTime(TreePIDs[Index],1,1);
    }

    return(NumberOfTreePIDs);
}
//---------------------------------------------------------------------------
void PrintTimes(char* Tag,float TreeCPUTime,float WCTime,unsigned long mem) {

    printf("%s: %.1f CPU %.1f WC %lu bytes mem (%.3f MB / %.3f GB)\n",Tag,TreeCPUTime,WCTime,mem,mem/1024.0/1024,mem/1024.0/1024/1024);
    fflush(stdout);

}
//---------------------------------------------------------------------------
float WallClockSoFar(struct timeval WCStartTime) {

    struct timeval WCEndTime;

    gettimeofday(&WCEndTime,NULL);
//DEBUG printf("Started at %ld +%f and ended at %ld +%f\n",
//DEBUG WCStartTime.tv_sec,WCStartTime.tv_usec/MICROSECONDS,
//DEBUG WCEndTime.tv_sec,WCEndTime.tv_usec/MICROSECONDS);

    return((WCEndTime.tv_sec - WCStartTime.tv_sec) +
(WCEndTime.tv_usec - WCStartTime.tv_usec)/MICROSECONDS);

}
//---------------------------------------------------------------------------
float WatchChildTree(int MyPID,int ChildPID,int CPUTimeLimit,
int DelayBetweenChecks,struct timeval WCStartTime,int PrintEachCheck) {

    float TreeTime,LastTreeTime;
    int NumberInTree;
    int KilledInTree;
    int printedTimeout = 0;

//----Initialize counters to 0
    TreeTime = 0;
    LastTreeTime = 0;
//----Loop watching times taken. Order is important - get time before
//----checking for interrupt
    do {
        sleep(DelayBetweenChecks);
//----Look at the tree
        NumberInTree = TimeTree(getuid(),ChildPID,&TreeTime);
        if (TreeTime > LastTreeTime) {
            LastTreeTime = TreeTime;
        }
//----Look at my children (in case they have all died)
        TreeTime = GetProcessTime(MyPID,0,1);
        if (TreeTime > LastTreeTime) {
            LastTreeTime = TreeTime;
        }

//DEBUG printf("TLR %d: Time = %.1f Greatest = %.1f\n",getpid(),TreeTime,LastTreeTime);

//----Print each loop if requested
        if (PrintEachCheck) {
            PrintTimes("WATCH",LastTreeTime,WallClockSoFar(WCStartTime),GetProcessMem(ChildPID));
        }

    } while ((CPUTimeLimit == 0 || LastTreeTime <= CPUTimeLimit) &&
NumberInTree > 0 && !GlobalInterrupted);

//----If over time limit, stop them all (XCPU to top guy first)
    if (NumberInTree > 0 && LastTreeTime > CPUTimeLimit) {
        KilledInTree = KillTree(getuid(),ChildPID,SIGXCPU);

	printedTimeout = 1;
	fprintf(stdout,"Timeout\n");
        fflush(stdout);
//DEBUG printf("Killed %d in tree\n",KilledInTree);
    }

//----If global interrupted, then send it on
    if (NumberInTree > 0 && GlobalInterrupted) {
	//fprintf(stdout,"Timeout\n");
        KilledInTree = KillTree(getuid(),ChildPID,GlobalSignalReceived);
//DEBUG printf("Killed %d in tree\n",KilledInTree);
	if (!printedTimeout) {
	  fprintf(stdout,"Timeout\n");
	  fflush(stdout);
	}
    }

    return(LastTreeTime);
}
//---------------------------------------------------------------------------
int main(int argc,char *argv[]) {

    int CPUTimeLimit;
    int WCTimeLimit;
    unsigned long MemoryLimit;
    int ArgNumber;
    int QuietnessLevel;
    int ArgOffset;
    pid_t ChildPID;
    float TreeCPUTime;
    float ChildTime;
    int DelayBetweenChecks;
    int PrintEachCheck = 0;
    ProcessDataArray SavePIDs;
    int NumberOfSavePIDs;

//----Check the quietness level
    if (argc >= 2 && strstr(argv[1],"-q") == argv[1]) {
        ArgOffset = 1;
        QuietnessLevel = atoi(&argv[ArgOffset][2]);
    } else {
        QuietnessLevel = 1;
        ArgOffset = 0;
    }

//----Look for time and print flags
    if (argc >= ArgOffset+2 &&
strstr(argv[ArgOffset+1],"-t") == argv[ArgOffset+1]) {
        ArgOffset++;
        DelayBetweenChecks = atoi(&argv[ArgOffset][2]);
    } else {
        if (argc >= ArgOffset+2 &&
strstr(argv[ArgOffset+1],"-p") == argv[ArgOffset+1]) {
            PrintEachCheck = 1;
            ArgOffset++;
            DelayBetweenChecks = atoi(&argv[ArgOffset][2]);
        } else {
            DelayBetweenChecks = DEFAULT_DELAY_BETWEEN_CHECKS;
        }
    }

    if (argc - ArgOffset >= 4) {
//----Redirect stderr to stdout
        //if (dup2(STDOUT,STDERR) == -1) {
         //   perror("ERROR: Cannot dup STDERR to STDOUT");
        //}

//----Extract time limits
        CPUTimeLimit = atoi(argv[ArgOffset+1]);
        WCTimeLimit = atoi(argv[ArgOffset+2]);
        if (isdigit((int)argv[ArgOffset+3][0])) {
            MemoryLimit = strtoul(argv[ArgOffset+3], 0, 0);
            ArgOffset++;
        } else {
            MemoryLimit = 0;
        }

        if (QuietnessLevel == 0) {
            printf(
"TreeLimitedRun: ----------------------------------------------------------\n");
            printf("TreeLimitedRun: %s ",argv[ArgOffset+3]);
            for (ArgNumber=ArgOffset+4;ArgNumber<argc;ArgNumber++)
                printf("%s ",argv[ArgNumber]);
            printf("\n");
            printf("TreeLimitedRun: CPU time limit is %ds\n",CPUTimeLimit);
            printf("TreeLimitedRun: WC  time limit is %ds\n",WCTimeLimit);
            if (MemoryLimit > 0) {
                printf("TreeLimitedRun: Memory   limit is %lu bytes\n",
MemoryLimit);
            }
//----Output the PID for possible later use
            printf("TreeLimitedRun: PID is %d\n",(int)getpid());
            printf(
"TimeLimitedRun: ----------------------------------------------------------\n");
            fflush(stdout);
        }
        SetNoCoreDump();

//----Set handler for when child dies
        if (signal(SIGCHLD,SIGCHLDHandler) == SIG_ERR) {
            perror("ERROR: Could not set SIGCHLD handler");
            exit(-1);
        }
//----Set handler for global interruptions and alarms
        if (signal(SIGQUIT,SIGQUITHandler) == SIG_ERR) {
            perror("ERROR: Could not set SIGQUIT handler");
            exit(-1);
        }
        if (signal(SIGALRM,SIGQUITHandler) == SIG_ERR) {
            perror("ERROR: Could not set SIGALRM handler");
            exit(-1);
        }

//----Record running processes at start (xeyes, gnome, etc)
        GetProcessesOwnedByMe(getuid(),SavePIDs,&NumberOfSavePIDs);

//----Fork for ATP process
        if ((ChildPID = fork()) == -1) {
            perror("ERROR: Cannot fork for ATP system process");
            exit(-1);
        }

//----Execute the ATP system
        if (ChildPID == 0) {
            if (setvbuf(stdout,NULL,_IONBF,0) != 0) {
                perror("Setting unbuffered");
            }
//DEBUG printf("The prover PID will be %d\n",getpid());
//----Set memory limit for child only
            if (MemoryLimit > 0) {
                SetMemoryLimit(MemoryLimit);
            }
//----In child
            execvp(argv[ArgOffset+3],argv+ArgOffset+3);
            perror("ERROR: TreeLimitRun cannot exec program:");
            exit(-1);

        } else {
            if (WCTimeLimit > 0) {
                alarm(WCTimeLimit);
            }
//----Record start time
            gettimeofday(&WCStartTime,NULL);
            TreeCPUTime = 0;
            WCTimeChild = 0;

//----Set global for interrupt handler
            GlobalInterrupted = 0;
            GlobalSignalReceived = 0;

//----Watch the tree of processes
            TreeCPUTime = WatchChildTree(getpid(),ChildPID,CPUTimeLimit,
DelayBetweenChecks,WCStartTime,PrintEachCheck);

//----Record end WC time
            // done in handler (otherwise affected by DelayBetweenChecks !!)
            //WCTimeChild = WallClockSoFar(WCStartTime);

//----See if the time is increased by looking at my children
            ChildTime = GetProcessTime(getpid(),0,1);
            if (ChildTime > TreeCPUTime) {
                TreeCPUTime = ChildTime;
            }

            // PrintTimes("FINAL WATCH",TreeCPUTime,WCTimeChild);
	    printf("%.1f\n",WCTimeChild);
	    fflush(stdout);

//----Sweep for orphans
//DEBUG printf("!!!Off to kill orphans\n");
            sleep(1);
            KillOrphans(getuid(),SavePIDs,NumberOfSavePIDs);
            sleep(1);
            KillOrphans(getuid(),SavePIDs,NumberOfSavePIDs);
        }
    } else {
        printf("Usage: %s [-q<quietness>] [-t<check delay>|-p<print check delay>] <CPU limit> <WC limit> [<Memory limit>] <Job>\n",
argv[0]);
    }

    return(0);
}
//---------------------------------------------------------------------------
