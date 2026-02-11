#include "systeminfo.h"
#include <QProcess>
#include <QFile>
#include <QTextStream>
#include <QDebug>
#include <QTimer>

SystemInfo::SystemInfo(QObject *parent) : QObject(parent)
{
    updateInfo();
    // Timer für regelmäßige Updates (alle 2 Sekunden)
    QTimer *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &SystemInfo::updateInfo);
    timer->start(2000);
}

QString SystemInfo::cpuUsage() const
{
    return m_cpuUsage;
}

QString SystemInfo::ramUsage() const
{
    return m_ramUsage;
}

QString SystemInfo::storageUsage() const
{
    return m_storageUsage;
}

void SystemInfo::updateInfo()
{
    // CPU Usage: Lies /proc/stat und berechne Auslastung
    static long prevTotal = 0, prevIdle = 0;
    QFile file("/proc/stat");
    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream in(&file);
        QString line = in.readLine();
        QStringList parts = line.split(" ", Qt::SkipEmptyParts);
        if (parts.size() > 7) {
            long user = parts[1].toLong();
            long nice = parts[2].toLong();
            long system = parts[3].toLong();
            long idle = parts[4].toLong();
            long iowait = parts[5].toLong();
            long irq = parts[6].toLong();
            long softirq = parts[7].toLong();
            long total = user + nice + system + idle + iowait + irq + softirq;

            if (prevTotal > 0) {
                long totalDiff = total - prevTotal;
                long idleDiff = idle - prevIdle;
                double usage = 100.0 * (totalDiff - idleDiff) / totalDiff;
                m_cpuUsage = QString("%1%").arg(usage, 0, 'f', 1);
            } else {
                m_cpuUsage = "0.0%"; // Erste Messung
            }
            prevTotal = total;
            prevIdle = idle;
        }
        file.close();
    }

    // RAM Usage: Lies /proc/meminfo
    QFile memFile("/proc/meminfo");
    if (memFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream memIn(&memFile);
        long totalMem = 0, availableMem = 0;
        while (!memIn.atEnd()) {
            QString memLine = memIn.readLine();
            if (memLine.startsWith("MemTotal:")) {
                totalMem = memLine.split(" ", Qt::SkipEmptyParts)[1].toLong();
            } else if (memLine.startsWith("MemAvailable:")) {
                availableMem = memLine.split(" ", Qt::SkipEmptyParts)[1].toLong();
            }
        }
        long usedMem = totalMem - availableMem;
        m_ramUsage = QString("%1 MB / %2 MB").arg(usedMem / 1024).arg(totalMem / 1024);
        memFile.close();
    }

    // Storage Usage: Verwende df /
    QProcess process;
    process.start("df", QStringList() << "/");
    process.waitForFinished();
    QString output = QString::fromLocal8Bit(process.readAllStandardOutput());
    QStringList lines = output.split("\n");
    if (lines.size() > 1) {
        QStringList parts = lines[1].split(" ", Qt::SkipEmptyParts);
        if (parts.size() > 4) {
            long used = parts[2].toLong() / 1024 / 1024; // GB
            long total = (parts[1].toLong() + parts[3].toLong()) / 1024 / 1024;
            m_storageUsage = QString("%1 GB / %2 GB").arg(used).arg(total);
        }
    }

    emit cpuUsageChanged();
    emit ramUsageChanged();
    emit storageUsageChanged();
}