"""Minimal Python 2 & 3 shim around all Qt bindings

DOCUMENTATION
    Qt.py was born in the film and visual effects industry to address
    the growing need for the development of software capable of running
    with more than one flavour of the Qt bindings for Python - PySide,
    PySide2, PyQt4 and PyQt5.

    1. Build for one, run with all
    2. Explicit is better than implicit
    3. Support co-existence

    Default resolution order:
        - PySide2
        - PyQt5
        - PySide6
        - PySide
        - PyQt4

    Usage:
        >> import sys
        >> from Qt import QtWidgets
        >> app = QtWidgets.QApplication(sys.argv)
        >> button = QtWidgets.QPushButton("Hello World")
        >> button.show()
        >> app.exec_()

    All members of PySide2 are mapped from other bindings, should they exist.
    If no equivalent member exist, it is excluded from Qt.py and inaccessible.
    The idea is to highlight members that exist across all supported binding,
    and guarantee that code that runs on one binding runs on all others.

    For more details, visit https://github.com/mottosso/Qt.py

LICENSE

    See end of file for license (MIT, BSD) information.

"""

import os
import sys
import types
import shutil
import importlib
import json


__version__ = "1.3.7"

# Enable support for `from Qt import *`
__all__ = []

# Flags from environment variables
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))
QT_PREFERRED_BINDING_JSON = os.getenv("QT_PREFERRED_BINDING_JSON", "")
QT_PREFERRED_BINDING = os.getenv("QT_PREFERRED_BINDING", "")
QT_SIP_API_HINT = os.getenv("QT_SIP_API_HINT")

# Reference to Qt.py
Qt = sys.modules[__name__]
Qt.QtCompat = types.ModuleType("QtCompat")

try:
    long
except NameError:
    # Python 3 compatibility
    long = int


"""Common members of all bindings

This is where each member of Qt.py is explicitly defined.
It is based on a "lowest common denominator" of all bindings;
including members found in each of the 4 bindings.

The "_common_members" dictionary is generated using the
build_membership.sh script.

"""

_common_members = {
    "QtCore": [
        "QAbstractAnimation",
        "QAbstractEventDispatcher",
        "QAbstractItemModel",
        "QAbstractListModel",
        "QAbstractState",
        "QAbstractTableModel",
        "QAbstractTransition",
        "QAnimationGroup",
        "QBasicTimer",
        "QBitArray",
        "QBuffer",
        "QByteArray",
        "QByteArrayMatcher",
        "QChildEvent",
        "QCoreApplication",
        "QCryptographicHash",
        "QDataStream",
        "QDate",
        "QDateTime",
        "QDir",
        "QDirIterator",
        "QDynamicPropertyChangeEvent",
        "QEasingCurve",
        "QElapsedTimer",
        "QEvent",
        "QEventLoop",
        "QEventTransition",
        "QFile",
        "QFileInfo",
        "QFileSystemWatcher",
        "QFinalState",
        "QGenericArgument",
        "QGenericReturnArgument",
        "QHistoryState",
        "QItemSelectionRange",
        "QIODevice",
        "QLibraryInfo",
        "QLine",
        "QLineF",
        "QLocale",
        "QMargins",
        "QMetaClassInfo",
        "QMetaEnum",
        "QMetaMethod",
        "QMetaObject",
        "QMetaProperty",
        "QMimeData",
        "QModelIndex",
        "QMutex",
        "QMutexLocker",
        "QObject",
        "QParallelAnimationGroup",
        "QPauseAnimation",
        "QPersistentModelIndex",
        "QPluginLoader",
        "QPoint",
        "QPointF",
        "QProcess",
        "QProcessEnvironment",
        "QPropertyAnimation",
        "QReadLocker",
        "QReadWriteLock",
        "QRect",
        "QRectF",
        "QRegExp",
        "QResource",
        "QRunnable",
        "QSemaphore",
        "QSequentialAnimationGroup",
        "QSettings",
        "QSignalMapper",
        "QSignalTransition",
        "QSize",
        "QSizeF",
        "QSocketNotifier",
        "QState",
        "QStateMachine",
        "QSysInfo",
        "QSystemSemaphore",
        "QT_TRANSLATE_NOOP",
        "QT_TR_NOOP",
        "QT_TR_NOOP_UTF8",
        "QTemporaryFile",
        "QTextBoundaryFinder",
        "QTextCodec",
        "QTextDecoder",
        "QTextEncoder",
        "QTextStream",
        "QTextStreamManipulator",
        "QThread",
        "QThreadPool",
        "QTime",
        "QTimeLine",
        "QTimer",
        "QTimerEvent",
        "QTranslator",
        "QUrl",
        "QVariantAnimation",
        "QWaitCondition",
        "QWriteLocker",
        "QXmlStreamAttribute",
        "QXmlStreamAttributes",
        "QXmlStreamEntityDeclaration",
        "QXmlStreamEntityResolver",
        "QXmlStreamNamespaceDeclaration",
        "QXmlStreamNotationDeclaration",
        "QXmlStreamReader",
        "QXmlStreamWriter",
        "Qt",
        "QtCriticalMsg",
        "QtDebugMsg",
        "QtFatalMsg",
        "QtMsgType",
        "QtSystemMsg",
        "QtWarningMsg",
        "qAbs",
        "qAddPostRoutine",
        "qChecksum",
        "qCritical",
        "qDebug",
        "qFatal",
        "qFuzzyCompare",
        "qIsFinite",
        "qIsInf",
        "qIsNaN",
        "qIsNull",
        "qRegisterResourceData",
        "qUnregisterResourceData",
        "qVersion",
        "qWarning",
        "qrand",
        "qsrand"
    ],
    "QtGui": [
        "QAbstractTextDocumentLayout",
        "QActionEvent",
        "QBitmap",
        "QBrush",
        "QClipboard",
        "QCloseEvent",
        "QColor",
        "QConicalGradient",
        "QContextMenuEvent",
        "QCursor",
        "QDesktopServices",
        "QDoubleValidator",
        "QDrag",
        "QDragEnterEvent",
        "QDragLeaveEvent",
        "QDragMoveEvent",
        "QDropEvent",
        "QFileOpenEvent",
        "QFocusEvent",
        "QFont",
        "QFontDatabase",
        "QFontInfo",
        "QFontMetrics",
        "QFontMetricsF",
        "QGradient",
        "QHelpEvent",
        "QHideEvent",
        "QHoverEvent",
        "QIcon",
        "QIconDragEvent",
        "QIconEngine",
        "QImage",
        "QImageIOHandler",
        "QImageReader",
        "QImageWriter",
        "QInputEvent",
        "QInputMethodEvent",
        "QIntValidator",
        "QKeyEvent",
        "QKeySequence",
        "QLinearGradient",
        "QMatrix2x2",
        "QMatrix2x3",
        "QMatrix2x4",
        "QMatrix3x2",
        "QMatrix3x3",
        "QMatrix3x4",
        "QMatrix4x2",
        "QMatrix4x3",
        "QMatrix4x4",
        "QMouseEvent",
        "QMoveEvent",
        "QMovie",
        "QPaintDevice",
        "QPaintEngine",
        "QPaintEngineState",
        "QPaintEvent",
        "QPainter",
        "QPainterPath",
        "QPainterPathStroker",
        "QPalette",
        "QPen",
        "QPicture",
        "QPictureIO",
        "QPixmap",
        "QPixmapCache",
        "QPolygon",
        "QPolygonF",
        "QQuaternion",
        "QRadialGradient",
        "QRegExpValidator",
        "QRegion",
        "QResizeEvent",
        "QSessionManager",
        "QShortcutEvent",
        "QShowEvent",
        "QStandardItem",
        "QStandardItemModel",
        "QStatusTipEvent",
        "QSyntaxHighlighter",
        "QTabletEvent",
        "QTextBlock",
        "QTextBlockFormat",
        "QTextBlockGroup",
        "QTextBlockUserData",
        "QTextCharFormat",
        "QTextCursor",
        "QTextDocument",
        "QTextDocumentFragment",
        "QTextFormat",
        "QTextFragment",
        "QTextFrame",
        "QTextFrameFormat",
        "QTextImageFormat",
        "QTextInlineObject",
        "QTextItem",
        "QTextLayout",
        "QTextLength",
        "QTextLine",
        "QTextList",
        "QTextListFormat",
        "QTextObject",
        "QTextObjectInterface",
        "QTextOption",
        "QTextTable",
        "QTextTableCell",
        "QTextTableCellFormat",
        "QTextTableFormat",
        "QTouchEvent",
        "QTransform",
        "QValidator",
        "QVector2D",
        "QVector3D",
        "QVector4D",
        "QWhatsThisClickedEvent",
        "QWheelEvent",
        "QWindowStateChangeEvent",
        "qAlpha",
        "qBlue",
        "qGray",
        "qGreen",
        "qIsGray",
        "qRed",
        "qRgb",
        "qRgba"
    ],
    "QtHelp": [
        "QHelpContentItem",
        "QHelpContentModel",
        "QHelpContentWidget",
        "QHelpEngine",
        "QHelpEngineCore",
        "QHelpIndexModel",
        "QHelpIndexWidget",
        "QHelpSearchEngine",
        "QHelpSearchQuery",
        "QHelpSearchQueryWidget",
        "QHelpSearchResultWidget"
    ],
    "QtMultimedia": [
        "QAbstractVideoBuffer",
        "QAbstractVideoSurface",
        "QAudio",
        "QAudioDeviceInfo",
        "QAudioFormat",
        "QAudioInput",
        "QAudioOutput",
        "QVideoFrame",
        "QVideoSurfaceFormat"
    ],
    "QtNetwork": [
        "QAbstractNetworkCache",
        "QAbstractSocket",
        "QAuthenticator",
        "QHostAddress",
        "QHostInfo",
        "QLocalServer",
        "QLocalSocket",
        "QNetworkAccessManager",
        "QNetworkAddressEntry",
        "QNetworkCacheMetaData",
        "QNetworkConfiguration",
        "QNetworkConfigurationManager",
        "QNetworkCookie",
        "QNetworkCookieJar",
        "QNetworkDiskCache",
        "QNetworkInterface",
        "QNetworkProxy",
        "QNetworkProxyFactory",
        "QNetworkProxyQuery",
        "QNetworkReply",
        "QNetworkRequest",
        "QNetworkSession",
        "QSsl",
        "QTcpServer",
        "QTcpSocket",
        "QUdpSocket"
    ],
    "QtOpenGL": [
        "QGL",
        "QGLContext",
        "QGLFormat",
        "QGLWidget"
    ],
    "QtPrintSupport": [
        "QAbstractPrintDialog",
        "QPageSetupDialog",
        "QPrintDialog",
        "QPrintEngine",
        "QPrintPreviewDialog",
        "QPrintPreviewWidget",
        "QPrinter",
        "QPrinterInfo"
    ],
    "QtSql": [
        "QSql",
        "QSqlDatabase",
        "QSqlDriver",
        "QSqlDriverCreatorBase",
        "QSqlError",
        "QSqlField",
        "QSqlIndex",
        "QSqlQuery",
        "QSqlQueryModel",
        "QSqlRecord",
        "QSqlRelation",
        "QSqlRelationalDelegate",
        "QSqlRelationalTableModel",
        "QSqlResult",
        "QSqlTableModel"
    ],
    "QtSvg": [
        "QGraphicsSvgItem",
        "QSvgGenerator",
        "QSvgRenderer",
        "QSvgWidget"
    ],
    "QtTest": [
        "QTest"
    ],
    "QtWidgets": [
        "QAbstractButton",
        "QAbstractGraphicsShapeItem",
        "QAbstractItemDelegate",
        "QAbstractItemView",
        "QAbstractScrollArea",
        "QAbstractSlider",
        "QAbstractSpinBox",
        "QActionGroup",
        "QApplication",
        "QBoxLayout",
        "QButtonGroup",
        "QCalendarWidget",
        "QCheckBox",
        "QColorDialog",
        "QColumnView",
        "QComboBox",
        "QCommandLinkButton",
        "QCommonStyle",
        "QCompleter",
        "QDataWidgetMapper",
        "QDateEdit",
        "QDateTimeEdit",
        "QDesktopWidget",
        "QDial",
        "QDialog",
        "QDialogButtonBox",
        "QDirModel",
        "QDockWidget",
        "QDoubleSpinBox",
        "QErrorMessage",
        "QFileDialog",
        "QFileIconProvider",
        "QFileSystemModel",
        "QFocusFrame",
        "QFontComboBox",
        "QFontDialog",
        "QFormLayout",
        "QFrame",
        "QGesture",
        "QGestureEvent",
        "QGestureRecognizer",
        "QGraphicsAnchor",
        "QGraphicsAnchorLayout",
        "QGraphicsBlurEffect",
        "QGraphicsColorizeEffect",
        "QGraphicsDropShadowEffect",
        "QGraphicsEffect",
        "QGraphicsEllipseItem",
        "QGraphicsGridLayout",
        "QGraphicsItem",
        "QGraphicsItemGroup",
        "QGraphicsLayout",
        "QGraphicsLayoutItem",
        "QGraphicsLineItem",
        "QGraphicsLinearLayout",
        "QGraphicsObject",
        "QGraphicsOpacityEffect",
        "QGraphicsPathItem",
        "QGraphicsPixmapItem",
        "QGraphicsPolygonItem",
        "QGraphicsProxyWidget",
        "QGraphicsRectItem",
        "QGraphicsRotation",
        "QGraphicsScale",
        "QGraphicsScene",
        "QGraphicsSceneContextMenuEvent",
        "QGraphicsSceneDragDropEvent",
        "QGraphicsSceneEvent",
        "QGraphicsSceneHelpEvent",
        "QGraphicsSceneHoverEvent",
        "QGraphicsSceneMouseEvent",
        "QGraphicsSceneMoveEvent",
        "QGraphicsSceneResizeEvent",
        "QGraphicsSceneWheelEvent",
        "QGraphicsSimpleTextItem",
        "QGraphicsTextItem",
        "QGraphicsTransform",
        "QGraphicsView",
        "QGraphicsWidget",
        "QGridLayout",
        "QGroupBox",
        "QHBoxLayout",
        "QHeaderView",
        "QInputDialog",
        "QItemDelegate",
        "QItemEditorCreatorBase",
        "QItemEditorFactory",
        "QKeyEventTransition",
        "QLCDNumber",
        "QLabel",
        "QLayout",
        "QLayoutItem",
        "QLineEdit",
        "QListView",
        "QListWidget",
        "QListWidgetItem",
        "QMainWindow",
        "QMdiArea",
        "QMdiSubWindow",
        "QMenu",
        "QMenuBar",
        "QMessageBox",
        "QMouseEventTransition",
        "QPanGesture",
        "QPinchGesture",
        "QPlainTextDocumentLayout",
        "QPlainTextEdit",
        "QProgressBar",
        "QProgressDialog",
        "QPushButton",
        "QRadioButton",
        "QRubberBand",
        "QScrollArea",
        "QScrollBar",
        "QShortcut",
        "QSizeGrip",
        "QSizePolicy",
        "QSlider",
        "QSpacerItem",
        "QSpinBox",
        "QSplashScreen",
        "QSplitter",
        "QSplitterHandle",
        "QStackedLayout",
        "QStackedWidget",
        "QStatusBar",
        "QStyle",
        "QStyleFactory",
        "QStyleHintReturn",
        "QStyleHintReturnMask",
        "QStyleHintReturnVariant",
        "QStyleOption",
        "QStyleOptionButton",
        "QStyleOptionComboBox",
        "QStyleOptionComplex",
        "QStyleOptionDockWidget",
        "QStyleOptionFocusRect",
        "QStyleOptionFrame",
        "QStyleOptionGraphicsItem",
        "QStyleOptionGroupBox",
        "QStyleOptionHeader",
        "QStyleOptionMenuItem",
        "QStyleOptionProgressBar",
        "QStyleOptionRubberBand",
        "QStyleOptionSizeGrip",
        "QStyleOptionSlider",
        "QStyleOptionSpinBox",
        "QStyleOptionTab",
        "QStyleOptionTabBarBase",
        "QStyleOptionTabWidgetFrame",
        "QStyleOptionTitleBar",
        "QStyleOptionToolBar",
        "QStyleOptionToolBox",
        "QStyleOptionToolButton",
        "QStyleOptionViewItem",
        "QStylePainter",
        "QStyledItemDelegate",
        "QSwipeGesture",
        "QSystemTrayIcon",
        "QTabBar",
        "QTabWidget",
        "QTableView",
        "QTableWidget",
        "QTableWidgetItem",
        "QTableWidgetSelectionRange",
        "QTapAndHoldGesture",
        "QTapGesture",
        "QTextBrowser",
        "QTextEdit",
        "QTimeEdit",
        "QToolBar",
        "QToolBox",
        "QToolButton",
        "QToolTip",
        "QTreeView",
        "QTreeWidget",
        "QTreeWidgetItem",
        "QTreeWidgetItemIterator",
        "QUndoCommand",
        "QUndoGroup",
        "QUndoStack",
        "QUndoView",
        "QVBoxLayout",
        "QWhatsThis",
        "QWidget",
        "QWidgetAction",
        "QWidgetItem",
        "QWizard",
        "QWizardPage"
    ],
    "QtX11Extras": [
        "QX11Info"
    ],
    "QtXml": [
        "QDomAttr",
        "QDomCDATASection",
        "QDomCharacterData",
        "QDomComment",
        "QDomDocument",
        "QDomDocumentFragment",
        "QDomDocumentType",
        "QDomElement",
        "QDomEntity",
        "QDomEntityReference",
        "QDomImplementation",
        "QDomNamedNodeMap",
        "QDomNode",
        "QDomNodeList",
        "QDomNotation",
        "QDomProcessingInstruction",
        "QDomText",
        "QXmlAttributes",
        "QXmlContentHandler",
        "QXmlDTDHandler",
        "QXmlDeclHandler",
        "QXmlDefaultHandler",
        "QXmlEntityResolver",
        "QXmlErrorHandler",
        "QXmlInputSource",
        "QXmlLexicalHandler",
        "QXmlLocator",
        "QXmlNamespaceSupport",
        "QXmlParseException",
        "QXmlReader",
        "QXmlSimpleReader"
    ],
    "QtXmlPatterns": [
        "QAbstractMessageHandler",
        "QAbstractUriResolver",
        "QAbstractXmlNodeModel",
        "QAbstractXmlReceiver",
        "QSourceLocation",
        "QXmlFormatter",
        "QXmlItem",
        "QXmlName",
        "QXmlNamePool",
        "QXmlNodeModelIndex",
        "QXmlQuery",
        "QXmlResultItems",
        "QXmlSchema",
        "QXmlSchemaValidator",
        "QXmlSerializer"
    ]
}

""" Missing members

This mapping describes members that have been deprecated
in one or more bindings and have been left out of the
_common_members mapping.

The member can provide an extra details string to be
included in exceptions and warnings.
"""

_missing_members = {
    "QtGui": {
        "QMatrix": "Deprecated in PyQt5",
    },
}


def _qInstallMessageHandler(handler):
    """Install a message handler that works in all bindings

    Args:
        handler: A function that takes 3 arguments, or None
    """
    def messageOutputHandler(*args):
        # In Qt4 bindings, message handlers are passed 2 arguments
        # In Qt5 bindings, message handlers are passed 3 arguments
        # The first argument is a QtMsgType
        # The last argument is the message to be printed
        # The Middle argument (if passed) is a QMessageLogContext
        if len(args) == 3:
            msgType, logContext, msg = args
        elif len(args) == 2:
            msgType, msg = args
            logContext = None
        else:
            raise TypeError(
                "handler expected 2 or 3 arguments, got {0}".format(len(args)))

        if isinstance(msg, bytes):
            # In python 3, some bindings pass a bytestring, which cannot be
            # used elsewhere. Decoding a python 2 or 3 bytestring object will
            # consistently return a unicode object.
            msg = msg.decode()

        handler(msgType, logContext, msg)

    passObject = messageOutputHandler if handler else handler
    if Qt.IsPySide or Qt.IsPyQt4:
        return Qt._QtCore.qInstallMsgHandler(passObject)
    elif Qt.IsPySide2 or Qt.IsPyQt5 or Qt.IsPySide6:
        return Qt._QtCore.qInstallMessageHandler(passObject)


def _getcpppointer(object):
    if hasattr(Qt, "_shiboken2"):
        return getattr(Qt, "_shiboken2").getCppPointer(object)[0]
    elif hasattr(Qt, "_shiboken"):
        return getattr(Qt, "_shiboken").getCppPointer(object)[0]
    elif hasattr(Qt, "_sip"):
        return getattr(Qt, "_sip").unwrapinstance(object)
    raise AttributeError("'module' has no attribute 'getCppPointer'")


def _wrapinstance(ptr, base=None):
    """Enable implicit cast of pointer to most suitable class

    This behaviour is available in sip per default.

    Based on http://nathanhorne.com/pyqtpyside-wrap-instance

    Usage:
        This mechanism kicks in under these circumstances.
        1. Qt.py is using PySide 1 or 2.
        2. A `base` argument is not provided.

        See :func:`QtCompat.wrapInstance()`

    Arguments:
        ptr (long): Pointer to QObject in memory
        base (QObject, optional): Base class to wrap with. Defaults to QObject,
            which should handle anything.

    """

    assert isinstance(ptr, long), "Argument 'ptr' must be of type <long>"
    assert (base is None) or issubclass(base, Qt.QtCore.QObject), (
        "Argument 'base' must be of type <QObject>")

    if Qt.IsPyQt4 or Qt.IsPyQt5:
        func = getattr(Qt, "_sip").wrapinstance
    elif Qt.IsPySide2:
        func = getattr(Qt, "_shiboken2").wrapInstance
    elif Qt.IsPySide6:
        func = getattr(Qt, "_shiboken6").wrapInstance
    elif Qt.IsPySide:
        func = getattr(Qt, "_shiboken").wrapInstance
    else:
        raise AttributeError("'module' has no attribute 'wrapInstance'")

    if base is None:
        if Qt.IsPyQt4 or Qt.IsPyQt5:
            base = Qt.QtCore.QObject
        else:
            q_object = func(long(ptr), Qt.QtCore.QObject)
            meta_object = q_object.metaObject()

            while True:
                class_name = meta_object.className()

                try:
                    base = getattr(Qt.QtWidgets, class_name)
                except AttributeError:
                    try:
                        base = getattr(Qt.QtCore, class_name)
                    except AttributeError:
                        meta_object = meta_object.superClass()
                        continue

                break

    return func(long(ptr), base)


def _isvalid(object):
    """Check if the object is valid to use in Python runtime.

    Usage:
        See :func:`QtCompat.isValid()`

    Arguments:
        object (QObject): QObject to check the validity of.

    """
    if hasattr(Qt, "_shiboken2"):
        return getattr(Qt, "_shiboken2").isValid(object)

    elif hasattr(Qt, "_shiboken"):
        return getattr(Qt, "_shiboken").isValid(object)

    elif hasattr(Qt, "_sip"):
        return not getattr(Qt, "_sip").isdeleted(object)

    else:
        raise AttributeError("'module' has no attribute isValid")


def _translate(context, sourceText, *args):
    # In Qt4 bindings, translate can be passed 2 or 3 arguments
    # In Qt5 bindings, translate can be passed 2 arguments
    # The first argument is disambiguation[str]
    # The last argument is n[int]
    # The middle argument can be encoding[QtCore.QCoreApplication.Encoding]
    if len(args) == 3:
        disambiguation, encoding, n = args
    elif len(args) == 2:
        disambiguation, n = args
        encoding = None
    else:
        raise TypeError(
            "Expected 4 or 5 arguments, got {0}.".format(len(args) + 2))

    if hasattr(Qt.QtCore, "QCoreApplication"):
        app = getattr(Qt.QtCore, "QCoreApplication")
    else:
        raise NotImplementedError(
            "Missing QCoreApplication implementation for {binding}".format(
                binding=Qt.__binding__,
            )
        )
    if Qt.__binding__ in ("PySide6", "PySide2", "PyQt5"):
        sanitized_args = [context, sourceText, disambiguation, n]
    else:
        sanitized_args = [
            context,
            sourceText,
            disambiguation,
            encoding or app.CodecForTr,
            n
        ]
    return app.translate(*sanitized_args)


def _loadUi(uifile, baseinstance=None):
    """Dynamically load a user interface from the given `uifile`

    This function calls `uic.loadUi` if using PyQt bindings,
    else it implements a comparable binding for PySide.

    Documentation:
        http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#PyQt5.uic.loadUi

    Arguments:
        uifile (str): Absolute path to Qt Designer file.
        baseinstance (QWidget): Instantiated QWidget or subclass thereof

    Return:
        baseinstance if `baseinstance` is not `None`. Otherwise
        return the newly created instance of the user interface.

    """
    if hasattr(Qt, "_uic"):
        return Qt._uic.loadUi(uifile, baseinstance)

    elif hasattr(Qt, "_QtUiTools"):
        # Implement `PyQt5.uic.loadUi` for PySide(2)

        class _UiLoader(Qt._QtUiTools.QUiLoader):
            """Create the user interface in a base instance.

            Unlike `Qt._QtUiTools.QUiLoader` itself this class does not
            create a new instance of the top-level widget, but creates the user
            interface in an existing instance of the top-level class if needed.

            This mimics the behaviour of `PyQt5.uic.loadUi`.

            """

            def __init__(self, baseinstance):
                super(_UiLoader, self).__init__(baseinstance)
                self.baseinstance = baseinstance
                self.custom_widgets = {}

            def _loadCustomWidgets(self, etree):
                """
                Workaround to pyside-77 bug.

                From QUiLoader doc we should use registerCustomWidget method.
                But this causes a segfault on some platforms.

                Instead we fetch from customwidgets DOM node the python class
                objects. Then we can directly use them in createWidget method.
                """

                def headerToModule(header):
                    """
                    Translate a header file to python module path
                    foo/bar.h => foo.bar
                    """
                    # Remove header extension
                    module = os.path.splitext(header)[0]

                    # Replace os separator by python module separator
                    return module.replace("/", ".").replace("\\", ".")

                custom_widgets = etree.find("customwidgets")

                if custom_widgets is None:
                    return

                for custom_widget in custom_widgets:
                    class_name = custom_widget.find("class").text
                    header = custom_widget.find("header").text
                    module = importlib.import_module(headerToModule(header))
                    self.custom_widgets[class_name] = getattr(module,
                                                              class_name)

            def load(self, uifile, *args, **kwargs):
                from xml.etree.ElementTree import ElementTree

                # For whatever reason, if this doesn't happen then
                # reading an invalid or non-existing .ui file throws
                # a RuntimeError.
                etree = ElementTree()
                etree.parse(uifile)
                self._loadCustomWidgets(etree)

                widget = Qt._QtUiTools.QUiLoader.load(
                    self, uifile, *args, **kwargs)

                # Workaround for PySide 1.0.9, see issue #208
                widget.parentWidget()

                return widget

            def createWidget(self, class_name, parent=None, name=""):
                """Called for each widget defined in ui file

                Overridden here to populate `baseinstance` instead.

                """

                if parent is None and self.baseinstance:
                    # Supposed to create the top-level widget,
                    # return the base instance instead
                    return self.baseinstance

                # For some reason, Line is not in the list of available
                # widgets, but works fine, so we have to special case it here.
                if class_name in self.availableWidgets() + ["Line"]:
                    # Create a new widget for child widgets
                    widget = Qt._QtUiTools.QUiLoader.createWidget(self,
                                                                  class_name,
                                                                  parent,
                                                                  name)
                elif class_name in self.custom_widgets:
                    widget = self.custom_widgets[class_name](parent=parent)
                else:
                    raise Exception("Custom widget '%s' not supported"
                                    % class_name)

                if self.baseinstance:
                    # Set an attribute for the new child widget on the base
                    # instance, just like PyQt5.uic.loadUi does.
                    setattr(self.baseinstance, name, widget)

                return widget

        widget = _UiLoader(baseinstance).load(uifile)
        Qt.QtCore.QMetaObject.connectSlotsByName(widget)

        return widget

    else:
        raise NotImplementedError("No implementation available for loadUi")


"""Misplaced members

These members from the original submodule are misplaced relative PySide2

"""
_misplaced_members = {
    "PySide6": {
        "QtCore.QStringListModel": "QtCore.QStringListModel",
        "QtGui.QStringListModel": "QtCore.QStringListModel",
        "QtCore.Property": "QtCore.Property",
        "QtCore.Signal": "QtCore.Signal",
        "QtCore.Slot": "QtCore.Slot",
        "QtCore.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
        "QtCore.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
        "QtCore.QItemSelection": "QtCore.QItemSelection",
        "QtCore.QItemSelectionModel": "QtCore.QItemSelectionModel",
        "QtCore.QItemSelectionRange": "QtCore.QItemSelectionRange",
        "QtUiTools.QUiLoader": ["QtCompat.loadUi", _loadUi],
        "shiboken6.wrapInstance": ["QtCompat.wrapInstance", _wrapinstance],
        "shiboken6.getCppPointer": ["QtCompat.getCppPointer", _getcpppointer],
        "shiboken6.isValid": ["QtCompat.isValid", _isvalid],
        "QtWidgets.qApp": "QtWidgets.QApplication.instance()",
        "QtCore.QCoreApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtWidgets.QApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtCore.qInstallMessageHandler": [
            "QtCompat.qInstallMessageHandler", _qInstallMessageHandler
        ],
        "QtWidgets.QStyleOptionViewItem": "QtCompat.QStyleOptionViewItemV4",
        "QtMultimedia.QSound": "QtMultimedia.QSound",
        "QtGui.QAction": "QtWidgets.QAction",
    },
    "PySide2": {
        "QtCore.QStringListModel": "QtCore.QStringListModel",
        "QtGui.QStringListModel": "QtCore.QStringListModel",
        "QtCore.Property": "QtCore.Property",
        "QtCore.Signal": "QtCore.Signal",
        "QtCore.Slot": "QtCore.Slot",
        "QtCore.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
        "QtCore.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
        "QtCore.QItemSelection": "QtCore.QItemSelection",
        "QtCore.QItemSelectionModel": "QtCore.QItemSelectionModel",
        "QtCore.QItemSelectionRange": "QtCore.QItemSelectionRange",
        "QtUiTools.QUiLoader": ["QtCompat.loadUi", _loadUi],
        "shiboken2.wrapInstance": ["QtCompat.wrapInstance", _wrapinstance],
        "shiboken2.getCppPointer": ["QtCompat.getCppPointer", _getcpppointer],
        "shiboken2.isValid": ["QtCompat.isValid", _isvalid],
        "QtWidgets.qApp": "QtWidgets.QApplication.instance()",
        "QtCore.QCoreApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtWidgets.QAction": "QtWidgets.QAction",
        "QtWidgets.QApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtCore.qInstallMessageHandler": [
            "QtCompat.qInstallMessageHandler", _qInstallMessageHandler
        ],
        "QtWidgets.QStyleOptionViewItem": "QtCompat.QStyleOptionViewItemV4",
        "QtMultimedia.QSound": "QtMultimedia.QSound",
    },
    "PyQt5": {
        "QtCore.pyqtProperty": "QtCore.Property",
        "QtCore.pyqtSignal": "QtCore.Signal",
        "QtCore.pyqtSlot": "QtCore.Slot",
        "QtCore.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
        "QtCore.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
        "QtCore.QStringListModel": "QtCore.QStringListModel",
        "QtCore.QItemSelection": "QtCore.QItemSelection",
        "QtCore.QItemSelectionModel": "QtCore.QItemSelectionModel",
        "QtCore.QItemSelectionRange": "QtCore.QItemSelectionRange",
        "uic.loadUi": ["QtCompat.loadUi", _loadUi],
        "sip.wrapinstance": ["QtCompat.wrapInstance", _wrapinstance],
        "sip.unwrapinstance": ["QtCompat.getCppPointer", _getcpppointer],
        "sip.isdeleted": ["QtCompat.isValid", _isvalid],
        "QtWidgets.qApp": "QtWidgets.QApplication.instance()",
        "QtCore.QCoreApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtWidgets.QAction": "QtWidgets.QAction",
        "QtWidgets.QApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtCore.qInstallMessageHandler": [
            "QtCompat.qInstallMessageHandler", _qInstallMessageHandler
        ],
        "QtWidgets.QStyleOptionViewItem": "QtCompat.QStyleOptionViewItemV4",
        "QtMultimedia.QSound": "QtMultimedia.QSound",
    },
    "PySide": {
        "QtGui.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
        "QtGui.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
        "QtGui.QStringListModel": "QtCore.QStringListModel",
        "QtGui.QItemSelection": "QtCore.QItemSelection",
        "QtGui.QItemSelectionModel": "QtCore.QItemSelectionModel",
        "QtCore.Property": "QtCore.Property",
        "QtCore.Signal": "QtCore.Signal",
        "QtCore.Slot": "QtCore.Slot",
        "QtGui.QItemSelectionRange": "QtCore.QItemSelectionRange",
        "QtGui.QAbstractPrintDialog": "QtPrintSupport.QAbstractPrintDialog",
        "QtGui.QPageSetupDialog": "QtPrintSupport.QPageSetupDialog",
        "QtGui.QPrintDialog": "QtPrintSupport.QPrintDialog",
        "QtGui.QPrintEngine": "QtPrintSupport.QPrintEngine",
        "QtGui.QPrintPreviewDialog": "QtPrintSupport.QPrintPreviewDialog",
        "QtGui.QPrintPreviewWidget": "QtPrintSupport.QPrintPreviewWidget",
        "QtGui.QPrinter": "QtPrintSupport.QPrinter",
        "QtGui.QPrinterInfo": "QtPrintSupport.QPrinterInfo",
        "QtUiTools.QUiLoader": ["QtCompat.loadUi", _loadUi],
        "shiboken.wrapInstance": ["QtCompat.wrapInstance", _wrapinstance],
        "shiboken.unwrapInstance": ["QtCompat.getCppPointer", _getcpppointer],
        "shiboken.isValid": ["QtCompat.isValid", _isvalid],
        "QtGui.qApp": "QtWidgets.QApplication.instance()",
        "QtCore.QCoreApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtGui.QApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtCore.qInstallMsgHandler": [
            "QtCompat.qInstallMessageHandler", _qInstallMessageHandler
        ],
        "QtGui.QStyleOptionViewItemV4": "QtCompat.QStyleOptionViewItemV4",
        "QtGui.QSound": "QtMultimedia.QSound",
    },
    "PyQt4": {
        "QtGui.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
        "QtGui.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
        "QtGui.QItemSelection": "QtCore.QItemSelection",
        "QtGui.QStringListModel": "QtCore.QStringListModel",
        "QtGui.QItemSelectionModel": "QtCore.QItemSelectionModel",
        "QtCore.pyqtProperty": "QtCore.Property",
        "QtCore.pyqtSignal": "QtCore.Signal",
        "QtCore.pyqtSlot": "QtCore.Slot",
        "QtGui.QItemSelectionRange": "QtCore.QItemSelectionRange",
        "QtGui.QAbstractPrintDialog": "QtPrintSupport.QAbstractPrintDialog",
        "QtGui.QPageSetupDialog": "QtPrintSupport.QPageSetupDialog",
        "QtGui.QPrintDialog": "QtPrintSupport.QPrintDialog",
        "QtGui.QPrintEngine": "QtPrintSupport.QPrintEngine",
        "QtGui.QPrintPreviewDialog": "QtPrintSupport.QPrintPreviewDialog",
        "QtGui.QPrintPreviewWidget": "QtPrintSupport.QPrintPreviewWidget",
        "QtGui.QPrinter": "QtPrintSupport.QPrinter",
        "QtGui.QPrinterInfo": "QtPrintSupport.QPrinterInfo",
        # "QtCore.pyqtSignature": "QtCore.Slot",
        "uic.loadUi": ["QtCompat.loadUi", _loadUi],
        "sip.wrapinstance": ["QtCompat.wrapInstance", _wrapinstance],
        "sip.unwrapinstance": ["QtCompat.getCppPointer", _getcpppointer],
        "sip.isdeleted": ["QtCompat.isValid", _isvalid],
        "QtCore.QString": "str",
        "QtGui.qApp": "QtWidgets.QApplication.instance()",
        "QtCore.QCoreApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtGui.QApplication.translate": [
            "QtCompat.translate", _translate
        ],
        "QtCore.qInstallMsgHandler": [
            "QtCompat.qInstallMessageHandler", _qInstallMessageHandler
        ],
        "QtGui.QStyleOptionViewItemV4": "QtCompat.QStyleOptionViewItemV4",
        "QtGui.QSound": "QtMultimedia.QSound",
    }
}

""" Compatibility Members

This dictionary is used to build Qt.QtCompat objects that provide a consistent
interface for obsolete members, and differences in binding return values.

{
    "binding": {
        "classname": {
            "targetname": "binding_namespace",
        }
    }
}
"""
_compatibility_members = {
    "PySide6": {
        "QWidget": {
            "grab": "QtWidgets.QWidget.grab",
        },
        "QHeaderView": {
            "sectionsClickable": "QtWidgets.QHeaderView.sectionsClickable",
            "setSectionsClickable":
                "QtWidgets.QHeaderView.setSectionsClickable",
            "sectionResizeMode": "QtWidgets.QHeaderView.sectionResizeMode",
            "setSectionResizeMode":
                "QtWidgets.QHeaderView.setSectionResizeMode",
            "sectionsMovable": "QtWidgets.QHeaderView.sectionsMovable",
            "setSectionsMovable": "QtWidgets.QHeaderView.setSectionsMovable",
        },
        "QFileDialog": {
            "getOpenFileName": "QtWidgets.QFileDialog.getOpenFileName",
            "getOpenFileNames": "QtWidgets.QFileDialog.getOpenFileNames",
            "getSaveFileName": "QtWidgets.QFileDialog.getSaveFileName",
        },
    },
    "PySide2": {
        "QWidget": {
            "grab": "QtWidgets.QWidget.grab",
        },
        "QHeaderView": {
            "sectionsClickable": "QtWidgets.QHeaderView.sectionsClickable",
            "setSectionsClickable":
                "QtWidgets.QHeaderView.setSectionsClickable",
            "sectionResizeMode": "QtWidgets.QHeaderView.sectionResizeMode",
            "setSectionResizeMode":
                "QtWidgets.QHeaderView.setSectionResizeMode",
            "sectionsMovable": "QtWidgets.QHeaderView.sectionsMovable",
            "setSectionsMovable": "QtWidgets.QHeaderView.setSectionsMovable",
        },
        "QFileDialog": {
            "getOpenFileName": "QtWidgets.QFileDialog.getOpenFileName",
            "getOpenFileNames": "QtWidgets.QFileDialog.getOpenFileNames",
            "getSaveFileName": "QtWidgets.QFileDialog.getSaveFileName",
        },
    },
    "PyQt5": {
        "QWidget": {
            "grab": "QtWidgets.QWidget.grab",
        },
        "QHeaderView": {
            "sectionsClickable": "QtWidgets.QHeaderView.sectionsClickable",
            "setSectionsClickable":
                "QtWidgets.QHeaderView.setSectionsClickable",
            "sectionResizeMode": "QtWidgets.QHeaderView.sectionResizeMode",
            "setSectionResizeMode":
                "QtWidgets.QHeaderView.setSectionResizeMode",
            "sectionsMovable": "QtWidgets.QHeaderView.sectionsMovable",
            "setSectionsMovable": "QtWidgets.QHeaderView.setSectionsMovable",
        },
        "QFileDialog": {
            "getOpenFileName": "QtWidgets.QFileDialog.getOpenFileName",
            "getOpenFileNames": "QtWidgets.QFileDialog.getOpenFileNames",
            "getSaveFileName": "QtWidgets.QFileDialog.getSaveFileName",
        },
    },
    "PySide": {
        "QWidget": {
            "grab": "QtWidgets.QPixmap.grabWidget",
        },
        "QHeaderView": {
            "sectionsClickable": "QtWidgets.QHeaderView.isClickable",
            "setSectionsClickable": "QtWidgets.QHeaderView.setClickable",
            "sectionResizeMode": "QtWidgets.QHeaderView.resizeMode",
            "setSectionResizeMode": "QtWidgets.QHeaderView.setResizeMode",
            "sectionsMovable": "QtWidgets.QHeaderView.isMovable",
            "setSectionsMovable": "QtWidgets.QHeaderView.setMovable",
        },
        "QFileDialog": {
            "getOpenFileName": "QtWidgets.QFileDialog.getOpenFileName",
            "getOpenFileNames": "QtWidgets.QFileDialog.getOpenFileNames",
            "getSaveFileName": "QtWidgets.QFileDialog.getSaveFileName",
        },
    },
    "PyQt4": {
        "QWidget": {
            "grab": "QtWidgets.QPixmap.grabWidget",
        },
        "QHeaderView": {
            "sectionsClickable": "QtWidgets.QHeaderView.isClickable",
            "setSectionsClickable": "QtWidgets.QHeaderView.setClickable",
            "sectionResizeMode": "QtWidgets.QHeaderView.resizeMode",
            "setSectionResizeMode": "QtWidgets.QHeaderView.setResizeMode",
            "sectionsMovable": "QtWidgets.QHeaderView.isMovable",
            "setSectionsMovable": "QtWidgets.QHeaderView.setMovable",
        },
        "QFileDialog": {
            "getOpenFileName": "QtWidgets.QFileDialog.getOpenFileName",
            "getOpenFileNames": "QtWidgets.QFileDialog.getOpenFileNames",
            "getSaveFileName": "QtWidgets.QFileDialog.getSaveFileName",
        },
    },
}


def _apply_site_config():
    try:
        import QtSiteConfig
    except ImportError:
        # If no QtSiteConfig module found, no modifications
        # to _common_members are needed.
        pass
    else:
        # Provide the ability to modify the dicts used to build Qt.py
        if hasattr(QtSiteConfig, 'update_members'):
            QtSiteConfig.update_members(_common_members)

        if hasattr(QtSiteConfig, 'update_misplaced_members'):
            QtSiteConfig.update_misplaced_members(members=_misplaced_members)

        if hasattr(QtSiteConfig, 'update_compatibility_members'):
            QtSiteConfig.update_compatibility_members(
                members=_compatibility_members)


def _new_module(name):
    return types.ModuleType(__name__ + "." + name)


def _import_sub_module(module, name):
    """import_sub_module will mimic the function of importlib.import_module"""
    module = __import__(module.__name__ + "." + name)
    for level in name.split("."):
        module = getattr(module, level)
    return module


def _setup(module, extras):
    """Install common submodules"""

    Qt.__binding__ = module.__name__

    def _warn_import_error(exc, module):
        msg = str(exc)
        if "No module named" in msg:
            return
        _warn("ImportError(%s): %s" % (module, msg))

    for name in list(_common_members) + extras:
        try:
            submodule = _import_sub_module(
                module, name)
        except ImportError as e:
            try:
                # For extra modules like sip and shiboken that may not be
                # children of the binding.
                submodule = __import__(name)
            except ImportError as e2:
                _warn_import_error(e, name)
                _warn_import_error(e2, name)
                continue

        setattr(Qt, "_" + name, submodule)

        if name not in extras:
            # Store reference to original binding,
            # but don't store speciality modules
            # such as uic or QtUiTools
            setattr(Qt, name, _new_module(name))


def _reassign_misplaced_members(binding):
    """Apply misplaced members from `binding` to Qt.py

    Arguments:
        binding (dict): Misplaced members

    """

    for src, dst in _misplaced_members[binding].items():
        dst_value = None

        src_parts = src.split(".")
        src_module = src_parts[0]
        src_member = None
        if len(src_parts) > 1:
            src_member = src_parts[1:]

        if isinstance(dst, (list, tuple)):
            dst, dst_value = dst

        dst_parts = dst.split(".")
        dst_module = dst_parts[0]
        dst_member = None
        if len(dst_parts) > 1:
            dst_member = dst_parts[1]

        # Get the member we want to store in the namesapce.
        if not dst_value:
            try:
                _part = getattr(Qt, "_" + src_module)
                while src_member:
                    member = src_member.pop(0)
                    _part = getattr(_part, member)
                dst_value = _part
            except AttributeError:
                # If the member we want to store in the namespace does not
                # exist, there is no need to continue. This can happen if a
                # request was made to rename a member that didn't exist, for
                # example if QtWidgets isn't available on the target platform.
                _log("Misplaced member has no source: {0}".format(src))
                continue

        try:
            src_object = getattr(Qt, dst_module)
        except AttributeError:
            if dst_module not in _common_members:
                # Only create the Qt parent module if its listed in
                # _common_members. Without this check, if you remove QtCore
                # from _common_members, the default _misplaced_members will add
                # Qt.QtCore so it can add Signal, Slot, etc.
                msg = 'Not creating missing member module "{m}" for "{c}"'
                _log(msg.format(m=dst_module, c=dst_member))
                continue
            # If the dst is valid but the Qt parent module does not exist
            # then go ahead and create a new module to contain the member.
            setattr(Qt, dst_module, _new_module(dst_module))
            src_object = getattr(Qt, dst_module)
            # Enable direct import of the new module
            sys.modules[__name__ + "." + dst_module] = src_object

        if not dst_value:
            dst_value = getattr(Qt, "_" + src_module)
            if src_member:
                dst_value = getattr(dst_value, src_member)

        setattr(
            src_object,
            dst_member or dst_module,
            dst_value
        )


def _build_compatibility_members(binding, decorators=None):
    """Apply `binding` to QtCompat

    Arguments:
        binding (str): Top level binding in _compatibility_members.
        decorators (dict, optional): Provides the ability to decorate the
            original Qt methods when needed by a binding. This can be used
            to change the returned value to a standard value. The key should
            be the classname, the value is a dict where the keys are the
            target method names, and the values are the decorator functions.

    """

    decorators = decorators or dict()

    # Allow optional site-level customization of the compatibility members.
    # This method does not need to be implemented in QtSiteConfig.
    try:
        import QtSiteConfig
    except ImportError:
        pass
    else:
        if hasattr(QtSiteConfig, 'update_compatibility_decorators'):
            QtSiteConfig.update_compatibility_decorators(binding, decorators)

    _QtCompat = type("QtCompat", (object,), {})

    for classname, bindings in _compatibility_members[binding].items():
        attrs = {}
        for target, binding in bindings.items():
            namespaces = binding.split('.')
            try:
                src_object = getattr(Qt, "_" + namespaces[0])
            except AttributeError as e:
                _log("QtCompat: AttributeError: %s" % e)
                # Skip reassignment of non-existing members.
                # This can happen if a request was made to
                # rename a member that didn't exist, for example
                # if QtWidgets isn't available on the target platform.
                continue

            # Walk down any remaining namespace getting the object assuming
            # that if the first namespace exists the rest will exist.
            for namespace in namespaces[1:]:
                src_object = getattr(src_object, namespace)

            # decorate the Qt method if a decorator was provided.
            if target in decorators.get(classname, []):
                # staticmethod must be called on the decorated method to
                # prevent a TypeError being raised when the decorated method
                # is called.
                src_object = staticmethod(
                    decorators[classname][target](src_object))

            attrs[target] = src_object

        # Create the QtCompat class and install it into the namespace
        compat_class = type(classname, (_QtCompat,), attrs)
        setattr(Qt.QtCompat, classname, compat_class)


def _pyside6():
    """Initialise PySide6

    These functions serve to test the existence of a binding
    along with set it up in such a way that it aligns with
    the final step; adding members from the original binding
    to Qt.py

    """

    import PySide6 as module
    extras = ["QtUiTools"]
    try:
        try:
            # Before merge of PySide and shiboken
            import shiboken6
        except ImportError:
            # After merge of PySide and shiboken, May 2017
            from PySide6 import shiboken6
        extras.append("shiboken6")
    except ImportError:
        pass

    _setup(module, extras)
    Qt.__binding_version__ = module.__version__

    if hasattr(Qt, "_shiboken6"):
        Qt.QtCompat.wrapInstance = _wrapinstance
        Qt.QtCompat.getCppPointer = _getcpppointer
        Qt.QtCompat.delete = shiboken6.delete

    if hasattr(Qt, "_QtUiTools"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtCore"):
        Qt.__qt_version__ = Qt._QtCore.qVersion()
        Qt.QtCompat.dataChanged = (
            lambda self, topleft, bottomright, roles=None:
            self.dataChanged.emit(topleft, bottomright, roles or [])
        )

    if hasattr(Qt, "_QtWidgets"):
        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtWidgets.QHeaderView.setSectionResizeMode

    _reassign_misplaced_members("PySide6")
    _build_compatibility_members("PySide6")


def _pyside2():
    """Initialise PySide2

    These functions serve to test the existence of a binding
    along with set it up in such a way that it aligns with
    the final step; adding members from the original binding
    to Qt.py

    """

    import PySide2 as module
    extras = ["QtUiTools"]
    try:
        try:
            # Before merge of PySide and shiboken
            import shiboken2
        except ImportError:
            # After merge of PySide and shiboken, May 2017
            from PySide2 import shiboken2
        extras.append("shiboken2")
    except ImportError:
        pass

    _setup(module, extras)
    Qt.__binding_version__ = module.__version__

    if hasattr(Qt, "_shiboken2"):
        Qt.QtCompat.wrapInstance = _wrapinstance
        Qt.QtCompat.getCppPointer = _getcpppointer
        Qt.QtCompat.delete = shiboken2.delete

    if hasattr(Qt, "_QtUiTools"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtCore"):
        Qt.__qt_version__ = Qt._QtCore.qVersion()
        Qt.QtCompat.dataChanged = (
            lambda self, topleft, bottomright, roles=None:
            self.dataChanged.emit(topleft, bottomright, roles or [])
        )

    if hasattr(Qt, "_QtWidgets"):
        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtWidgets.QHeaderView.setSectionResizeMode

    _reassign_misplaced_members("PySide2")
    _build_compatibility_members("PySide2")


def _pyside():
    """Initialise PySide"""

    import PySide as module
    extras = ["QtUiTools"]
    try:
        try:
            # Before merge of PySide and shiboken
            import shiboken
        except ImportError:
            # After merge of PySide and shiboken, May 2017
            from PySide import shiboken
        extras.append("shiboken")
    except ImportError:
        pass

    _setup(module, extras)
    Qt.__binding_version__ = module.__version__

    if hasattr(Qt, "_shiboken"):
        Qt.QtCompat.wrapInstance = _wrapinstance
        Qt.QtCompat.getCppPointer = _getcpppointer
        Qt.QtCompat.delete = shiboken.delete

    if hasattr(Qt, "_QtUiTools"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtGui"):
        setattr(Qt, "QtWidgets", _new_module("QtWidgets"))
        setattr(Qt, "_QtWidgets", Qt._QtGui)
        if hasattr(Qt._QtGui, "QX11Info"):
            setattr(Qt, "QtX11Extras", _new_module("QtX11Extras"))
            Qt.QtX11Extras.QX11Info = Qt._QtGui.QX11Info

        Qt.QtCompat.setSectionResizeMode = Qt._QtGui.QHeaderView.setResizeMode

    if hasattr(Qt, "_QtCore"):
        Qt.__qt_version__ = Qt._QtCore.qVersion()
        Qt.QtCompat.dataChanged = (
            lambda self, topleft, bottomright, roles=None:
            self.dataChanged.emit(topleft, bottomright)
        )

    _reassign_misplaced_members("PySide")
    _build_compatibility_members("PySide")


def _pyqt5():
    """Initialise PyQt5"""

    import PyQt5 as module
    extras = ["uic"]

    try:
        # Relevant to PyQt5 5.11 and above
        from PyQt5 import sip
        extras += ["sip"]
    except ImportError:

        try:
            import sip
            extras += ["sip"]
        except ImportError:
            sip = None

    _setup(module, extras)
    if hasattr(Qt, "_sip"):
        Qt.QtCompat.wrapInstance = _wrapinstance
        Qt.QtCompat.getCppPointer = _getcpppointer
        Qt.QtCompat.delete = sip.delete

    if hasattr(Qt, "_uic"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtCore"):
        Qt.__binding_version__ = Qt._QtCore.PYQT_VERSION_STR
        Qt.__qt_version__ = Qt._QtCore.QT_VERSION_STR
        Qt.QtCompat.dataChanged = (
            lambda self, topleft, bottomright, roles=None:
            self.dataChanged.emit(topleft, bottomright, roles or [])
        )

    if hasattr(Qt, "_QtWidgets"):
        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtWidgets.QHeaderView.setSectionResizeMode

    _reassign_misplaced_members("PyQt5")
    _build_compatibility_members('PyQt5')


def _pyqt4():
    """Initialise PyQt4"""

    import sip

    # Validation of envivornment variable. Prevents an error if
    # the variable is invalid since it's just a hint.
    try:
        hint = int(QT_SIP_API_HINT)
    except TypeError:
        hint = None  # Variable was None, i.e. not set.
    except ValueError:
        raise ImportError("QT_SIP_API_HINT=%s must be a 1 or 2")

    for api in ("QString",
                "QVariant",
                "QDate",
                "QDateTime",
                "QTextStream",
                "QTime",
                "QUrl"):
        try:
            sip.setapi(api, hint or 2)
        except AttributeError:
            raise ImportError("PyQt4 < 4.6 isn't supported by Qt.py")
        except ValueError:
            actual = sip.getapi(api)
            if not hint:
                raise ImportError("API version already set to %d" % actual)
            else:
                # Having provided a hint indicates a soft constraint, one
                # that doesn't throw an exception.
                sys.stderr.write(
                    "Warning: API '%s' has already been set to %d.\n"
                    % (api, actual)
                )

    import PyQt4 as module
    extras = ["uic"]
    try:
        import sip
        extras.append(sip.__name__)
    except ImportError:
        sip = None

    _setup(module, extras)
    if hasattr(Qt, "_sip"):
        Qt.QtCompat.wrapInstance = _wrapinstance
        Qt.QtCompat.getCppPointer = _getcpppointer
        Qt.QtCompat.delete = sip.delete

    if hasattr(Qt, "_uic"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtGui"):
        setattr(Qt, "QtWidgets", _new_module("QtWidgets"))
        setattr(Qt, "_QtWidgets", Qt._QtGui)
        if hasattr(Qt._QtGui, "QX11Info"):
            setattr(Qt, "QtX11Extras", _new_module("QtX11Extras"))
            Qt.QtX11Extras.QX11Info = Qt._QtGui.QX11Info

        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtGui.QHeaderView.setResizeMode

    if hasattr(Qt, "_QtCore"):
        Qt.__binding_version__ = Qt._QtCore.PYQT_VERSION_STR
        Qt.__qt_version__ = Qt._QtCore.QT_VERSION_STR
        Qt.QtCompat.dataChanged = (
            lambda self, topleft, bottomright, roles=None:
            self.dataChanged.emit(topleft, bottomright)
        )

    _reassign_misplaced_members("PyQt4")

    # QFileDialog QtCompat decorator
    def _standardizeQFileDialog(some_function):
        """Decorator that makes PyQt4 return conform to other bindings"""
        def wrapper(*args, **kwargs):
            ret = (some_function(*args, **kwargs))

            # PyQt4 only returns the selected filename, force it to a
            # standard return of the selected filename, and a empty string
            # for the selected filter
            return ret, ''

        wrapper.__doc__ = some_function.__doc__
        wrapper.__name__ = some_function.__name__

        return wrapper

    decorators = {
        "QFileDialog": {
            "getOpenFileName": _standardizeQFileDialog,
            "getOpenFileNames": _standardizeQFileDialog,
            "getSaveFileName": _standardizeQFileDialog,
        }
    }
    _build_compatibility_members('PyQt4', decorators)


def _none():
    """Internal option (used in installer)"""

    Mock = type("Mock", (), {"__getattr__": lambda Qt, attr: None})

    Qt.__binding__ = "None"
    Qt.__qt_version__ = "0.0.0"
    Qt.__binding_version__ = "0.0.0"
    Qt.QtCompat.loadUi = lambda uifile, baseinstance=None: None
    Qt.QtCompat.setSectionResizeMode = lambda *args, **kwargs: None

    for submodule in _common_members.keys():
        setattr(Qt, submodule, Mock())
        setattr(Qt, "_" + submodule, Mock())


def _log(text):
    if QT_VERBOSE:
        sys.stdout.write("Qt.py [info]: %s\n" % text)


def _warn(text):
    if QT_VERBOSE:
        try:
            sys.stderr.write("Qt.py [warning]: %s\n" % text)
        except UnicodeDecodeError:
            import locale
            encoding = locale.getpreferredencoding()
            sys.stderr.write("Qt.py [warning]: %s\n" % text.decode(encoding))


def _convert(lines):
    """Convert compiled .ui file from PySide2 to Qt.py

    Arguments:
        lines (list): Each line of of .ui file

    Usage:
        >> with open("myui.py") as f:
        ..   lines = _convert(f.readlines())

    """

    def parse(line):
        line = line.replace("from PySide2 import", "from Qt import QtCompat,")
        line = line.replace("QtWidgets.QApplication.translate",
                            "QtCompat.translate")
        if "QtCore.SIGNAL" in line:
            raise NotImplementedError("QtCore.SIGNAL is missing from PyQt5 "
                                      "and so Qt.py does not support it: you "
                                      "should avoid defining signals inside "
                                      "your ui files.")
        return line

    parsed = list()
    for line in lines:
        line = parse(line)
        parsed.append(line)

    return parsed


def _cli(args):
    """Qt.py command-line interface"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--convert",
                        help="Path to compiled Python module, e.g. my_ui.py")
    parser.add_argument("--compile",
                        help="Accept raw .ui file and compile with native "
                             "PySide2 compiler.")
    parser.add_argument("--stdout",
                        help="Write to stdout instead of file",
                        action="store_true")
    parser.add_argument("--stdin",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)

    if args.stdout:
        raise NotImplementedError("--stdout")

    if args.stdin:
        raise NotImplementedError("--stdin")

    if args.compile:
        raise NotImplementedError("--compile")

    if args.convert:
        sys.stdout.write("#\n"
                         "# WARNING: --convert is an ALPHA feature.\n#\n"
                         "# See https://github.com/mottosso/Qt.py/pull/132\n"
                         "# for details.\n"
                         "#\n")

        #
        # ------> Read
        #
        with open(args.convert) as f:
            lines = _convert(f.readlines())

        backup = "%s_backup%s" % os.path.splitext(args.convert)
        sys.stdout.write("Creating \"%s\"..\n" % backup)
        shutil.copy(args.convert, backup)

        #
        # <------ Write
        #
        with open(args.convert, "w") as f:
            f.write("".join(lines))

        sys.stdout.write("Successfully converted \"%s\"\n" % args.convert)


class MissingMember(object):
    """
    A placeholder type for a missing Qt object not
    included in Qt.py

    Args:
        name (str): The name of the missing type
        details (str): An optional custom error message
    """
    ERR_TMPL = ("{} is not a common object across PySide2 "
                "and the other Qt bindings. It is not included "
                "as a common member in the Qt.py layer")

    def __init__(self, name, details=''):
        self.__name = name
        self.__err = self.ERR_TMPL.format(name)

        if details:
            self.__err = "{}: {}".format(self.__err, details)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.__name)

    def __getattr__(self, name):
        raise NotImplementedError(self.__err)

    def __call__(self, *a, **kw):
        raise NotImplementedError(self.__err)


def _install():
    # Default order (customize order and content via QT_PREFERRED_BINDING)
    default_order = ("PySide2", "PyQt5", "PySide6", "PySide", "PyQt4")
    preferred_order = None
    if QT_PREFERRED_BINDING_JSON:
        # A per-vendor preferred binding customization was defined
        # This should be a dictionary of the full Qt.py module namespace to
        # apply binding settings to. The "default" key can be used to apply
        # custom bindings to all modules not explicitly defined. If the json
        # data is invalid this will raise a exception.
        # Example:
        #   {"mylibrary.vendor.Qt": ["PySide2"], "default":["PyQt5","PyQt4"]}
        try:
            preferred_bindings = json.loads(QT_PREFERRED_BINDING_JSON)
        except ValueError:
            # Python 2 raises ValueError, Python 3 raises json.JSONDecodeError
            # a subclass of ValueError
            _warn("Failed to parse QT_PREFERRED_BINDING_JSON='%s'"
                  % QT_PREFERRED_BINDING_JSON)
            _warn("Falling back to default preferred order")
        else:
            preferred_order = preferred_bindings.get(__name__)
            # If no matching binding was used, optionally apply a default.
            if preferred_order is None:
                preferred_order = preferred_bindings.get("default", None)
    if preferred_order is None:
        # If a json preferred binding was not used use, respect the
        # QT_PREFERRED_BINDING environment variable if defined.
        preferred_order = list(
            b for b in QT_PREFERRED_BINDING.split(os.pathsep) if b
        )

    order = preferred_order or default_order

    available = {
        "PySide6": _pyside6,
        "PySide2": _pyside2,
        "PyQt5": _pyqt5,
        "PySide": _pyside,
        "PyQt4": _pyqt4,
        "None": _none
    }

    _log("Order: '%s'" % "', '".join(order))

    # Allow site-level customization of the available modules.
    _apply_site_config()

    found_binding = False
    for name in order:
        _log("Trying %s" % name)

        try:
            available[name]()
            found_binding = True
            break

        except ImportError as e:
            _log("ImportError: %s" % e)

        except KeyError:
            _log("ImportError: Preferred binding '%s' not found." % name)

    if not found_binding:
        # If not binding were found, throw this error
        raise ImportError("No Qt binding were found.")

    # Install individual members
    for name, members in _common_members.items():
        try:
            their_submodule = getattr(Qt, "_%s" % name)
        except AttributeError:
            continue

        our_submodule = getattr(Qt, name)

        # Enable import *
        __all__.append(name)

        # Enable direct import of submodule,
        # e.g. import Qt.QtCore
        sys.modules[__name__ + "." + name] = our_submodule

        for member in members:
            # Accept that a submodule may miss certain members.
            try:
                their_member = getattr(their_submodule, member)
            except AttributeError:
                _log("'%s.%s' was missing." % (name, member))
                continue

            setattr(our_submodule, member, their_member)

    # Install missing member placeholders
    for name, members in _missing_members.items():
        our_submodule = getattr(Qt, name)

        for member in members:

            # If the submodule already has this member installed,
            # either by the common members, or the site config,
            # then skip installing this one over it.
            if hasattr(our_submodule, member):
                continue

            placeholder = MissingMember("{}.{}".format(name, member),
                                        details=members[member])
            setattr(our_submodule, member, placeholder)

    # Enable direct import of QtCompat
    sys.modules[__name__ + ".QtCompat"] = Qt.QtCompat

    # Backwards compatibility
    if hasattr(Qt.QtCompat, 'loadUi'):
        Qt.QtCompat.load_ui = Qt.QtCompat.loadUi


_install()

# Setup Binding Enum states
Qt.IsPySide2 = Qt.__binding__ == 'PySide2'
Qt.IsPyQt5 = Qt.__binding__ == 'PyQt5'
Qt.IsPySide6 = Qt.__binding__ == 'PySide6'
Qt.IsPySide = Qt.__binding__ == 'PySide'
Qt.IsPyQt4 = Qt.__binding__ == 'PyQt4'

"""Augment QtCompat

QtCompat contains wrappers and added functionality
to the original bindings, such as the CLI interface
and otherwise incompatible members between bindings,
such as `QHeaderView.setSectionResizeMode`.

"""

Qt.QtCompat._cli = _cli
Qt.QtCompat._convert = _convert

# Enable command-line interface
if __name__ == "__main__":
    _cli(sys.argv[1:])


# The MIT License (MIT)
#
# Copyright (c) 2016-2017 Marcus Ottosson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# In PySide(2), loadUi does not exist, so we implement it
#
# `_UiLoader` is adapted from the qtpy project, which was further influenced
# by qt-helpers which was released under a 3-clause BSD license which in turn
# is based on a solution at:
#
# - https://gist.github.com/cpbotha/1b42a20c8f3eb9bb7cb8
#
# The License for this code is as follows:
#
# qt-helpers - a common front-end to various Qt modules
#
# Copyright (c) 2015, Chris Beaumont and Thomas Robitaille
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the Glue project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Which itself was based on the solution at
#
# https://gist.github.com/cpbotha/1b42a20c8f3eb9bb7cb8
#
# which was released under the MIT license:
#
# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@gmail.com>
# Modifications by Charl Botha <cpbotha@vxlabs.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files
# (the "Software"),to deal in the Software without restriction,
# including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
