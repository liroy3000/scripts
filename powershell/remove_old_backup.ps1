# Скрипт удаления устаревших бэкапов
#
# Предполагается, что есть папки для хранения бэкапов баз данных. Одна папка для бэкапов одной базы. Каждая папка содержит в себе подпапки с датой в имени и содержащей в себе сам дамп базы.
# Сценарий удалит подпапки, срок жизни которых больше, чем указан в переменной $period

# Внесите в массив все пути, где хранятся бэкапы:

$targets = @(
"c:\backup\base1\",
"c:\backup\base2\"
)

$period = "-30"

$current_day = Get-Date
$day_del = $current_day.AddDays($period)

function remove_backup($target_folder) {
    
    $dirs = Get-ChildItem $target_folder
    cd $target_folder
    foreach ($dir in $dirs) {
    	if ($dir.LastWriteTime -lt $day_del) {
        	Remove-Item $dir -Recurse
        }
    }
}

foreach ($target in $targets) {
	remove_backup($target)
}