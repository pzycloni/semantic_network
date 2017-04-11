from math import sqrt, ceil

class Node:

	def __init__(self, name, link = False):
		self.name = name
		# является ли узел ссылкой
		self.is_link = link


class Tree:

	def __init__(self):
		self.nodes = dict()


	# добавление узлов и связей в дерево
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
	def filter(self, question_word, data_word):
		# если количество букв в корне больше 3х,
		# то обрезаем слово(приблизительно выделяем корень)
		if len(question_word) >= 3:
			last_index = ceil(sqrt(len(question_word))) + 1
		else:
			last_index = len(question_word)
		# сравниваем корни(вхождения)
		if self.__compare(question_word[0:last_index], data_word):
			return True

		return False


	# число вхождений слов
	def get_count_concurrences(self, question, line):
		count = 0

		for question_word in question.split():
			for line_word in line:
				# сравниваем корни слова
				if self.filter(question_word, line_word.name):
					count += 1

				

		return count


	# число вхождений букв
	def get_count_concurrences_alphabet(self, question, line):
		concurrences = list()

		for question_word in question.split():
			for answer_word in line:
				if self.filter(question_word, answer_word.name):
					for i in range(min([len(answer_word.name), len(question_word)])):
						temp = self.__compare(answer_word.name[i], question_word[i])
						# как только встретили несоответствие, 
						# прерываем сравнение букв слов
						if temp == False:
							break
						# количество вхождений
						concurrences.append(temp)

		return len(concurrences)	


	# все узлы графа
	def get_list_nodes(self):
		children = list()

		for parent in self.nodes:
			for child in self.nodes[parent]:
				if child not in children:
					children.append(child)

		return children


	# обход графа по узлам
	def traversal(self, start, end, path = []):

		path = path + [start]

		if start == end:
			return path

		if start not in self.nodes:
			return None

		for node in self.nodes[start]:
			if node not in path:
				newpath = self.traversal(node, end, path)

				if newpath:
					return newpath

		return None


	# поиск ответа на вопрос
	def find(self, question):
		nodes  = list()
		result = list()
		concurrences = list()

		list_nodes = self.get_list_nodes()

		# выбираем узлы, 
		# которые совпадают со словами в вопросе 
		for word in question.split():
			for node in list_nodes:
				# сравниваем корень слова в узле 
				# и корень слова в вопросе
				if self.filter(word, node.name):
					if node not in nodes:
						nodes.append(node)
						# если слово в узле это связь,
						# то берем все узлы с этой связью
						if node.is_link:
							for child in self.nodes[node]:
								if child not in nodes:
									nodes.append(child)

		# обход графа по найденным узлам, 
		# т.е. ищем все пути между узлами
		for start in range(len(nodes)):
			for end in range(len(nodes)):
				output = self.traversal(nodes[start], nodes[end])
				if output:
					result.append(output)
		
		temp = list()
		# проверяем сколько слов из вопроса 
		# содержится в каждом найденном пути
		for line in result:
			temp.append(self.get_count_concurrences(question, line))
		# выбираем максимальное количество содержащихся слов
		max_count_compare = max(temp)

		# получем все пути с максимальным числов вхождений
		# ---------от--------- 
		indexes = [i for i, value in enumerate(temp) if max_count_compare == value]
		lines = list()
		for i in indexes:
			if len(result[i]) > 1:
				lines.append(result[i])
		# ---------до---------

		# сохраняем первичные найденные данные
		first_result = result

		# находим максимальное число вхождений букв вопроса 
		# в каждом слове из каждого пути
		for line in lines:
			count = 0
			for line_node in line:
				# считаем число входящих букв
				count += self.get_count_concurrences_alphabet(question, line)

			concurrences.append(count)

		# выбираем максимальное количество содержащихся букв
		max_count_compare = max(concurrences)
		# получем все пути с максимальным числов вхождений
		# ---------от--------- 
		indexes = [i for i, value in enumerate(concurrences) if max_count_compare == value or max_count_compare - len(lines) == value]

		result = list()
		for i in indexes:
			result.append(lines[i])
		# ---------до---------

		# проверка на идентичность
		# проверяем, не потярян ли правильный ответ
		update = list()
		for line in result:
			for row in first_result:
				count = 0
				if len(line) == len(row):
					# считаем количество вхождений 
					# первичного результата в ответе
					for i in range(len(line)):
						res = self.__compare(line[i].name, row[i].name)
						# если количество равных элементов на один меньше, 
						# чем количество в ответе,
						# то добавляем эти элементы в ответ
						if count + 1 == len(line):
							update.append(row[i])
						# как только находим несоответствие - обрываем поиск
						if not res:
							break
						# количество вхождений
						count += 1
		# применяем обновления	
		result.append(update)

		return result


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

	question1 = "Какой двигатель имеют автомашины"
	question2 = "Что использует поезд для передвижения"
	question3 = "Кем управляется морское транспортное средство"
	question4 = "Кем управляется яхта"
	question5 = "Является ли самолет транспортным средством"
	question6 = "По каким дорогам двигается локомотив"
	question7 = "Существует ли такое транспортное средство, которое управляется пилотом и передвигается с помощью реактивных двигателей"
	question8 = "Самолет это транспортное средство"
	question9 = "Локомотив это поезд"

	# запуск поиска ответа на вопрос
	question = question5.lower()
	result = tree.find(question)

	# распечатка ответа
	for line in result:
		print([node.name for node in line])
