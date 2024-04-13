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
        twisted = dnstwist.run(domain=domain, registered=True, threads=40)

        i = 0
        for data in twisted:
            dnstwistData.append(data)
            i += 1

    return dnstwistData

def cleanupPermutations(data: list) -> list:
    dataToWrite = []
    currentDomain = 0

    for entry in data:
        currentDomain += 1

        if not 'dns_a' in entry:
            continue
        
        dnsName = entry['domain']
        aRecord = entry['dns_a'][0]
        nsRecord = ''

        if 'dns_ns' in entry:
            nsRecord = entry['dns_ns'][0]

        if currentDomain == 1:
            originalIP = aRecord
            originalNS = nsRecord

            continue

        if aRecord == "0.0.0.0" or aRecord == "127.0.0.1":
            continue

        if aRecord == '!ServFail':
            continue

        if aRecord == originalIP or nsRecord == originalNS:
            continue

        domainComment = "# " + dnsName + " - " + nsRecord
        dataToWrite.append(domainComment)
        dataToWrite.append(aRecord)

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
    clearFile = open(file, "w")
    clearFile.write("")
    clearFile.close()

    feedFile = open(file, "a")
    
    for line in dataToWrite:
        feedFile.write(line + "\n")

    feedFile.close()

    return True

if __name__ == '__main__':
    domainsFile = "conf/small-domains.txt"
    feedFile = "feed/feed.txt"

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

    print(f"Complete.")

    sys.exit(0)