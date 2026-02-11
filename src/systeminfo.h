#ifndef SYSTEMINFO_H
#define SYSTEMINFO_H

#include <QObject>
#include <QString>

class SystemInfo : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString cpuUsage READ cpuUsage NOTIFY cpuUsageChanged)
    Q_PROPERTY(QString ramUsage READ ramUsage NOTIFY ramUsageChanged)
    Q_PROPERTY(QString storageUsage READ storageUsage NOTIFY storageUsageChanged)

public:
    explicit SystemInfo(QObject *parent = nullptr);

    QString cpuUsage() const;
    QString ramUsage() const;
    QString storageUsage() const;

    void updateInfo();  // Für Tests public machen

signals:
    void cpuUsageChanged();
    void ramUsageChanged();
    void storageUsageChanged();

private:
    QString m_cpuUsage;
    QString m_ramUsage;
    QString m_storageUsage;
};

#endif // SYSTEMINFO_H