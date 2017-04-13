from math import sqrt, ceil

# узел
class Node:

	def __init__(self, name, link = False):
		# содержимое узла
		self.name = name
		# является ли узел связью
		self.is_link = link

# граф представлен в виде словаря
# {
#	parent: [child1, child2, ..., child8],
#	child2: [child3, child7],
#	..
# }

class Tree:

	def __init__(self):
		# граф
		self.nodes = dict()

	# добавление узлов и связей в граф
	def add(self, link, parent, child):
		if parent not in self.nodes:
			self.nodes[parent] = list()

		if link not in self.nodes:
			self.nodes[link] = list()

		self.nodes[parent].append(link)
		self.nodes[link].append(child)

	# проверяем, входит ли одно слово
	# в другое или наоборот
	def __compare(self, word1, word2):

		if word1.find(word2) >= 0:
			return True

		if word2.find(word1) >= 0:
			return True

		return False

	# ищем примерный корень слова
	def is_same_root(self, question_word, data_word):
		if len(question_word) >= 3:
			last_index = ceil(sqrt(len(question_word))) + 1
		else:
			last_index = len(question_word)
		# сравниваем
		if self.__compare(question_word[0:last_index], data_word):
			return True

		return False

	# число совпадающих слов
	def count_concurrences(self, question, path):
		counter = 0

		for question_word in question.split():
			for path_word in path:
				# ищем однокоренные слова
				if self.is_same_root(question_word, path_word.name):
					counter += 1

		return counter

	# число совпадающих букв
	def count_concurrences_alphabet(self, question, path):
		concurrences = list()

		for question_word in question.split():
			for answer_word in path:
				# проверяем, чтобы слова были однокоренными
				if self.is_same_root(question_word, answer_word.name):
		
					min_length = min([len(answer_word.name), len(question_word)])
					for i in range(min_length):
						# сравниваем по буквам однокоренные слова
						temp = self.__compare(answer_word.name[i], question_word[i])
						# как только встретили несоответствие, 
						# прерываем сравнение по буквам для пары слов
						# и начинаем делать тоже самое для другой пары
						# однокоренных слов
						if temp == False:
							break
						# запоминаем количество совпавших букв
						concurrences.append(temp)

		return len(concurrences)

	# все узлы графа
	def get_list_nodes(self):
		nodes = list()

		for parent in self.nodes:
			for node in self.nodes[parent]:
				if node not in nodes:
					nodes.append(node)

		return nodes

	# обход графа по узлам
	def traversal(self, start, end, path = []):

		path = path + [start]
		# если путь существует,
		# то возвращаем его
		if start == end:
			return path

		if start not in self.nodes:
			return None
		# рекурсивный обход
		for node in self.nodes[start]:
			if node not in path:
				newpath = self.traversal(node, end, path)

				if newpath:
					return newpath

		return None

	# поиск ответа на вопрос
	def find(self, question):
		question = question.lower()
		# узлы, с однокренными словами
		nodes  = list()
		# все узлы графа
		list_nodes = self.get_list_nodes()

		# выбираем узлы, 
		# которые совпадают со словами в впоросе 
		for word in question.split():
			for node in list_nodes:
				# находим однокоренные слова
				# в вопросе и в графе
				if self.is_same_root(word, node.name):
					if node not in nodes:
						nodes.append(node)
						# если слово в узле это связь,
						# то берем все узлы с этой связью
						if node.is_link:
							for child in self.nodes[node]:
								if child not in nodes:
									nodes.append(child)

		paths = list()
		# обход графа по найденным узлам, 
		# т.е. ищем все возможные пути между узлами
		for start in range(len(nodes)):
			for end in range(len(nodes)):
				if start != end:
					path = self.traversal(nodes[start], nodes[end])
					if path:
						paths.append(path)

		concurrences = list()
		# проверяем сколько слов из вопроса 
		# содержится в каждом найденном пути
		for path in paths:
			counter = 0

			for node in path:
				counter += self.count_concurrences(question, path)

			concurrences.append(counter)
		# выбираем максимальное количество содержащихся слов
		max_counter = max(concurrences)

		# получем все пути с максимальным числов вхождений
		# ---------от--------- 
		indexes = [i for i, value in enumerate(concurrences) if max_counter == value]

		lines = list()
		for index in indexes:
			# отбрасываем пути,
			# которые имеют только один узел
			if len(paths[index]) > 1:
				lines.append(paths[index])
		# ---------до---------

		# сохраняем первичные найденные данные,
		# т.к. впоследствии может быть потерян 
		# один из верных ответов
		first_paths = paths

		concurrences = list()
		# находим максимальное число совпадений букв вопроса 
		# и букв слов в найденных узлах для каждого пути line
		for line in lines:
			# считаем число входящих букв
			counter = self.count_concurrences_alphabet(question, line)

			concurrences.append(counter)

		# выбираем максимальное количество содержащихся букв
		max_counter = max(concurrences)
		# получем все пути с максимальным числов вхождений
		# ---------от--------- 
		indexes = [i for i, value in enumerate(concurrences) if max_counter == value]

		paths = list()
		for index in indexes:
			paths.append(lines[index])
		# ---------до---------

		# проверка на идентичность
		# проверяем, не потярян ли правильный ответ
		update = list()
		for path in paths:
			for row in first_paths:

				length = 0
				if len(path) == len(row):
					# считаем количество вхождений 
					# первичного результата в ответе
					for number in range(len(path)):
						res = self.__compare(path[number].name, row[number].name)
						# если количество равных элементов на один меньше, 
						# чем количество в ответе,
						# то добавляем эти элементы в ответ
						if length + 1 == len(path):
							update.append(row[number])
						# как только находим несоответствие - обрываем поиск
						if not res:
							break
						# количество вхождений
						length += 1
		# применяем обновления	
		paths.append(update)

		return paths



def load_base():

	# основные узлы
	people = Node("люди")
	transport = Node("транспортные средства")
	land = Node("сухопутные")
	sea = Node("морские")
	air = Node("воздушные")
	circle = Node("колеса")
	road = Node("специальным дорогам")
	train = Node("поезда")
	auto = Node("автомашины")
	rails = Node("железнодорожным рельсам")
	motorway = Node("автодорогам")
	machinist = Node("машинист")
	driver = Node("водитель")
	disel_motor = Node("дизельные двигатели")
	elec_motor = Node("электрические двигатели")
	elec_train = Node("электропоезд")
	locomotive = Node("локомотив")
	petrol_motor = Node("бензиновые двигатели")
	capitan = Node("капитан")
	boat = Node("катер")
	yacht = Node("яхта")
	react_motor = Node("реативные двигатели")
	pilot = Node("пилот")
	helicopter = Node("вертолет")
	plan = Node("самолет")
	screw = Node("винт")

	tree = Tree()

	# узлы и связи
	tree.add(Node("для передвижения используют", True), people, transport)
	tree.add(Node("можно разделить на", True), transport, land)
	tree.add(Node("можно разделить на", True), transport, sea)
	tree.add(Node("можно разделить на", True), transport, air)
	tree.add(Node("существует", True), transport, land)
	tree.add(Node("существует", True), transport, sea)
	tree.add(Node("существует", True), transport, air)
	tree.add(Node("для передвижения используют", True), land, circle)
	tree.add(Node("передвигаются по", True), land, road)
	tree.add(Node("являются", True), transport, train)
	tree.add(Node("являются", True), transport, auto)
	tree.add(Node("передвигаются по", True), train, rails)
	tree.add(Node("передвигаются по", True), auto, motorway)
	tree.add(Node("управляет", True), train, machinist)
	tree.add(Node("управляет", True), auto, driver)
	tree.add(Node("имеет", True), train, disel_motor)
	tree.add(Node("имеет", True), train, elec_motor)
	tree.add(Node("это", True), train, locomotive)
	tree.add(Node("двигается по", True), locomotive, rails)
	tree.add(Node("это", True), train, elec_train)
	tree.add(Node("используют", True), auto, petrol_motor)
	tree.add(Node("используют", True), auto, disel_motor)
	tree.add(Node("для движения использует", True), sea, screw)
	tree.add(Node("являются", True), sea, boat)
	tree.add(Node("управляет", True), yacht, capitan)
	tree.add(Node("управляет", True), boat, capitan)
	tree.add(Node("являются", True), sea, yacht)
	tree.add(Node("передвигается с помощью", True), air, react_motor)
	tree.add(Node("управляет движением", True), transport, pilot)
	tree.add(Node("это", True), air, plan)
	tree.add(Node("это", True), air, helicopter)

	return tree

if __name__ == '__main__':
	# собираем наш граф
	tree = load_base()

	question1 = "Какой двигатель имеют автомашины?"
	question2 = "Что использует поезд для передвижения?"
	question3 = "Кем управляется морское транспортное средство?"
	question4 = "Кем управляется яхта?"
	question5 = "Является ли самолет транспортным средством?"
	question6 = "По каким дорогам двигается локомотив?"
	question7 = "Существует ли такое транспортное средство, которое управляется пилотом и передвигается с помощью реактивных двигателей?"
	question8 = "Самолет это транспортное средство?"
	question9 = "Локомотив это поезд?"

	# запуск поиска ответа на вопрос
	answers = tree.find(question2)

	# распечатка ответа
	for answer in answers:
		print([node.name for node in answer])