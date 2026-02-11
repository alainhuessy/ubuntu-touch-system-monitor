/****************************************************************************
** Meta object code from reading C++ file 'systeminfo.h'
**
** Created by: The Qt Meta Object Compiler version 68 (Qt 6.4.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../../src/systeminfo.h"
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'systeminfo.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 68
#error "This file was generated using the moc from 6.4.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace {
struct qt_meta_stringdata_SystemInfo_t {
    uint offsetsAndSizes[16];
    char stringdata0[11];
    char stringdata1[16];
    char stringdata2[1];
    char stringdata3[16];
    char stringdata4[20];
    char stringdata5[9];
    char stringdata6[9];
    char stringdata7[13];
};
#define QT_MOC_LITERAL(ofs, len) \
    uint(sizeof(qt_meta_stringdata_SystemInfo_t::offsetsAndSizes) + ofs), len 
Q_CONSTINIT static const qt_meta_stringdata_SystemInfo_t qt_meta_stringdata_SystemInfo = {
    {
        QT_MOC_LITERAL(0, 10),  // "SystemInfo"
        QT_MOC_LITERAL(11, 15),  // "cpuUsageChanged"
        QT_MOC_LITERAL(27, 0),  // ""
        QT_MOC_LITERAL(28, 15),  // "ramUsageChanged"
        QT_MOC_LITERAL(44, 19),  // "storageUsageChanged"
        QT_MOC_LITERAL(64, 8),  // "cpuUsage"
        QT_MOC_LITERAL(73, 8),  // "ramUsage"
        QT_MOC_LITERAL(82, 12)   // "storageUsage"
    },
    "SystemInfo",
    "cpuUsageChanged",
    "",
    "ramUsageChanged",
    "storageUsageChanged",
    "cpuUsage",
    "ramUsage",
    "storageUsage"
};
#undef QT_MOC_LITERAL
} // unnamed namespace

Q_CONSTINIT static const uint qt_meta_data_SystemInfo[] = {

 // content:
      10,       // revision
       0,       // classname
       0,    0, // classinfo
       3,   14, // methods
       3,   35, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags, initial metatype offsets
       1,    0,   32,    2, 0x06,    4 /* Public */,
       3,    0,   33,    2, 0x06,    5 /* Public */,
       4,    0,   34,    2, 0x06,    6 /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

 // properties: name, type, flags
       5, QMetaType::QString, 0x00015001, uint(0), 0,
       6, QMetaType::QString, 0x00015001, uint(1), 0,
       7, QMetaType::QString, 0x00015001, uint(2), 0,

       0        // eod
};

Q_CONSTINIT const QMetaObject SystemInfo::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_SystemInfo.offsetsAndSizes,
    qt_meta_data_SystemInfo,
    qt_static_metacall,
    nullptr,
    qt_incomplete_metaTypeArray<qt_meta_stringdata_SystemInfo_t,
        // property 'cpuUsage'
        QtPrivate::TypeAndForceComplete<QString, std::true_type>,
        // property 'ramUsage'
        QtPrivate::TypeAndForceComplete<QString, std::true_type>,
        // property 'storageUsage'
        QtPrivate::TypeAndForceComplete<QString, std::true_type>,
        // Q_OBJECT / Q_GADGET
        QtPrivate::TypeAndForceComplete<SystemInfo, std::true_type>,
        // method 'cpuUsageChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'ramUsageChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'storageUsageChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>
    >,
    nullptr
} };

void SystemInfo::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<SystemInfo *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->cpuUsageChanged(); break;
        case 1: _t->ramUsageChanged(); break;
        case 2: _t->storageUsageChanged(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (SystemInfo::*)();
            if (_t _q_method = &SystemInfo::cpuUsageChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (SystemInfo::*)();
            if (_t _q_method = &SystemInfo::ramUsageChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (SystemInfo::*)();
            if (_t _q_method = &SystemInfo::storageUsageChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 2;
                return;
            }
        }
    }else if (_c == QMetaObject::ReadProperty) {
        auto *_t = static_cast<SystemInfo *>(_o);
        (void)_t;
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< QString*>(_v) = _t->cpuUsage(); break;
        case 1: *reinterpret_cast< QString*>(_v) = _t->ramUsage(); break;
        case 2: *reinterpret_cast< QString*>(_v) = _t->storageUsage(); break;
        default: break;
        }
    } else if (_c == QMetaObject::WriteProperty) {
    } else if (_c == QMetaObject::ResetProperty) {
    } else if (_c == QMetaObject::BindableProperty) {
    }
    (void)_a;
}

const QMetaObject *SystemInfo::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *SystemInfo::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_SystemInfo.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int SystemInfo::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 3)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 3;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 3)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 3;
    }else if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::BindableProperty
            || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 3;
    }
    return _id;
}

// SIGNAL 0
void SystemInfo::cpuUsageChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void SystemInfo::ramUsageChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void SystemInfo::storageUsageChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
