import dnstwist
import sys
import datetime

def getDomains(file: str) -> list:
    domainsFile = open(file, "r")
    domains = domainsFile.readlines()
    domainsFile.close()

    return domains

def runPermutations(domains: list) -> list:
    dnstwistData = []

    for domain in domains:
        twisted = dnstwist.run(domain=domain, registered=True, threads=80, all=True)

        i = 0
        for data in twisted:
            dnstwistData.append(data)
            i += 1

    return dnstwistData

def cleanupPermutations(data: list) -> list:
    dataToWrite = []

    for entry in data:

        needToContinue = 0

        if not 'dns_a' in entry:
            continue
        
        dnsName = entry['domain']
        aRecord = entry['dns_a']
        nsRecord = []

        if 'dns_ns' in entry:
            nsRecord = entry['dns_ns']

        if entry['fuzzer'] == "*original":
            originalIP = aRecord
            originalNS = nsRecord

            continue

        if "0.0.0.0" in aRecord or "127.0.0.1" in aRecord:
            continue

        if '!ServFail' in aRecord:
            continue
        
        for record in aRecord:
            if record in originalIP:
                needToContinue = 1

        for record in nsRecord:
            if record in originalNS:
                needToContinue = 1

        if needToContinue == 1:
            continue

        nsRecords = ""
        for record in nsRecord:
            nsRecords = nsRecords + record + " "
        
        domainComment = " # " + dnsName + " - " + nsRecords
        for record in aRecord:
            dataToWrite.append(record + domainComment)

    return dataToWrite

def backupFeed(file: str) -> bool:
    backupDate = datetime.date.today()
    backupDate = backupDate.isoformat()
    backupName = file + ".bak-" + backupDate

    feedFile = open(file, "r")
    data = feedFile.readlines()
    feedFile.close()

    backupFile = open(backupName, "w")
    backupFile.write("# Backup taken on " + backupDate)
    for line in data:
        backupFile.write(line)

    return True

def writeFeed(file: str, dataToWrite: list) -> bool:
    writeTime = datetime.datetime.now()

    clearFile = open(file, "w")
    clearFile.write("")
    clearFile.close()

    feedFile = open(file, "a")
    
    feedFile.write("# Feed last refreshed on " + writeTime.isoformat)

    for line in dataToWrite:
        if isinstance(line, list):
            line = line[0]
        feedFile.write(line + "\n")

    feedFile.close()

    return True

def getRunTime(starttime: datetime.time, endtime: datetime.time) -> float:
    startDelta = datetime.timedelta(hours=starttime.hour, minutes=starttime.minute, seconds=starttime.second)
    endDelta = datetime.timedelta(hours=endtime.hour, minutes=endtime.minute, seconds=endtime.second)

    totalRunTime = endDelta - startDelta

    return totalRunTime

if __name__ == '__main__':
    domainsFile = "/root/conf/domains.txt"
    feedFile = "/root/feed/feed.txt"

    startTime = datetime.datetime.now()
    print(f"Feed refresh started at {startTime.hour}:{startTime.minute}:{startTime.second}")

    print(f"Reading domain file at {domainsFile}")
    domains = getDomains(domainsFile)

    print(f"Permutating domains...")
    permutations = runPermutations(domains)

    print(f"Cleaning up data...")
    dataToWrite = cleanupPermutations(permutations)

    print(f"Backing up current feed file...")
    backupFeed(feedFile)

    print(f"Writing to feed file at {feedFile}...")
    writeFeed(feedFile, dataToWrite)

    endTime = datetime.datetime.now()
    totalRunTime = getRunTime(startTime, endTime)
    print(f"Feed refresh completed. Total runtime: {totalRunTime}")

    sys.exit(0)