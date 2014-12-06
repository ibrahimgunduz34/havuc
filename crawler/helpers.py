import importlib


def load_class(full_class_path):
	splitted_class_path = full_class_path.split('.')
	moduleName = '.'.join(splitted_class_path[0:-1])
	if splitted_class_path.count > 1:
		className = splitted_class_path[-1]
		module = importlib.import_module(moduleName)
		if not hasattr(module, className):
			raise ImportError(
				'No class exists %s in %s' % (className, moduleName))
		return getattr(module, className)
	else:
		return importlib.import_module(moduleName)


def load_resource(resource_name):
	class_path = 'crawler.resources.%s' % resource_name
	return load_class(class_path)