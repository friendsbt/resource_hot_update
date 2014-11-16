from resource_hot_update import HotUpdate

def update():
	update = HotUpdate()
	update.run(update.update_hot_day)
	update.run(update.get_hottest_resource)
	update.backup_hot_resource()

if __name__ == "__main__":
	update()  
