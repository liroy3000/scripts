import os
import datetime
import subprocess
"""
Скрипт для удаления устаревших снапшотов.
В системе хранится два вида снапшотов zfs:
Ежечастные, которые создаются с 10 до 20 часов, и ежедневные, которые создаются в 23:00
Все снапшоты имеют одинаковую маску имени, и хранятся в одном каталоге, поэтому чтобы определить тип снапшота необходимо смотреть на время его создания.
Ежечастные снапшоты должны храниться 7 дней, ежедневные - 30.
"""


def remove_snp(filename):
	"""
	Функция, удаляющая выбранный снапшот.
	Обязательный аргумент - имя файла.
	"""
	snapname = 'pool0/storage@' + filename
	subprocess.call(['zfs', 'destroy', snapname])


files = os.listdir('/pool0/storage/.zfs/snapshot')							# Получим список файлов снапшотов
now = datetime.datetime.now()												# Текущее время

for i in files:
	try:
		filedate = datetime.datetime.strptime(str(i), '%Y-%m-%d_%H.%M')		# Преобразуем имя файла в дату
	except ValueError:														# Если имя файла не соответсвует маске - останавливаем итерацию и переходим к следующему файлу
		continue
	delta = now - filedate													# Вычисляем время жизни снапшота
	if filedate.hour < 21:													# Если время создания снапшота < 21 часа - значит снапшот ежечастный
			if delta.days > 7:												# Если время жизни более недели, удаляем его
				remove_snp(str(i))
	else:																	# Если снапшот был сделан после 21:00 - значит снапшот ежедневный (ночной)
		if delta.days > 30:													# Если время жизни более 30 дней, удаляем его.
			remove_snp(str(i))

