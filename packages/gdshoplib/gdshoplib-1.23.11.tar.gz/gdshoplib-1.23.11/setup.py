# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdshoplib',
 'gdshoplib.activities',
 'gdshoplib.apps',
 'gdshoplib.apps.crm',
 'gdshoplib.apps.delivery',
 'gdshoplib.apps.finance',
 'gdshoplib.apps.marketing',
 'gdshoplib.apps.payments',
 'gdshoplib.apps.platforms',
 'gdshoplib.apps.products',
 'gdshoplib.apps.uploader',
 'gdshoplib.cli',
 'gdshoplib.cli.crm',
 'gdshoplib.cli.finance',
 'gdshoplib.cli.product',
 'gdshoplib.cli.service',
 'gdshoplib.cli.temporal',
 'gdshoplib.core',
 'gdshoplib.packages',
 'gdshoplib.services',
 'gdshoplib.services.avito',
 'gdshoplib.services.gdshop',
 'gdshoplib.services.notion',
 'gdshoplib.services.notion.models',
 'gdshoplib.services.vk',
 'gdshoplib.services.ym',
 'gdshoplib.workflows']

package_data = \
{'': ['*'], 'gdshoplib': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Pillow>=9.3.0,<10.0.0',
 'backoff>=2.2.1,<3.0.0',
 'boto3>=1.26.32,<2.0.0',
 'isort>=5.10.1,<6.0.0',
 'kafka-python>=2.0.2,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.9.1,<5.0.0',
 'msgpack>=1.0.5,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-barcode>=0.14.0,<0.15.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-magic>=0.4.27,<0.5.0',
 'pyzbar>=0.1.9,<0.2.0',
 'qrcode[pil]>=7.4.2,<8.0.0',
 'redis>=4.3.5,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'temporalio>=1.2.0,<2.0.0',
 'twine>=4.0.1,<5.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'ujson>=5.7.0,<6.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['gdshoplib = gdshoplib:application']}

setup_kwargs = {
    'name': 'gdshoplib',
    'version': '1.23.11',
    'description': '',
    'long_description': '# Библиотека для управления магазином gdshop\n\nПользовательские объекты для высокоуровневой работы без привязки к слою данных. Предоставляет Python like интерфейс для работы с объектами\n\n## Finance\n\n- [ ] Информация о состоянии счетов\n- [ ] Операций с финансами\n- [ ] Статистика по финансам за периоды + Прогнозы\n- [ ] Расчет и контроль бюджетов\n- [ ] Сбор информации с площадок по финансам\n- [ ] Генерация отчетов\n- [x] Балловый метод ценообразования\n\n## Marketing\n\n- [ ] Статистика рекламных компаний\n- [ ] Управление рекламными компаниями\n- [ ] Статистика воронок\n- [ ] Выгрузка информации с площадок\n- [ ] Генерация отчетов\n- [ ] Статистика по товарам\n\n## Order\n- [ ] Получение информации о заказах\n\n## Product\n- [x] Получение информации о продукте\n- [ ] Обновление содержимого продукта\n- [x] Выгрузка информации о товаре в фид\n- [ ] Работа с закупками\n- [ ] Оценка материалов\n- [x] Работа с media\n- [x] Работа с description\n- [x] Выгрузка меда в S3\n\n## Platform\n- [x] Генерация товарных фидов\n\n\n# Полезные ссылки\n\n## Описание товарного фида\n\nhttps://yandex.ru/support/partnermarket/export/yml.html\nhttps://drive.google.com/file/d/1kkKa0KU7iNOszyC2oQSGmHNwp3sRGKFb/view\n\n\n# FAQ\n\nImportError: Unable to find zbar shared library\n\n```\nmkdir ~/lib\nln -s $(brew --prefix zbar)/lib/libzbar.dylib ~/lib/libzbar.dylib\n```',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
