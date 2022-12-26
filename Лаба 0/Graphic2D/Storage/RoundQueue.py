from Graphic2D.Storage.Element import Element, Node


class RoundQueue:
    def __init__(self, lst=None):
        self.__head, self.__tail = None, None
        self.__size = 0
        if not(lst is None):
            for value in lst[::-1]:
                self.push(value)

    def __len__(self):
        return self.__size

    def push(self, elem):
        if self.__head is None:
            self.__head = Node(elem)
        elif self.__size == 1:
            self.__head = Node(elem, self.__head)
            self.__tail = self.__head.next
            self.__tail.next = self.__head
        else:
            self.__head = Node(elem, self.__head)
            self.__tail.next = self.__head
        self.__size += 1

    def peek(self):
        if self.__head is None:
            return None
        return self.__head.data

    def pop(self):
        if not(self.__head is None):
            if self.__size >= 3:
                self.__head = self.__head.next
                self.__tail.next = self.__head
            elif self.__size == 2:
                self.__head = self.__head.next
                self.__head.next = None
                self.__tail = None
            elif self.__size == 1:
                self.__head = None
            self.__size -= 1

    def twist(self):
        if self.__size > 1:
            self.__head = self.__head.next
            self.__tail = self.__tail.next

    def to_list(self):
        if self.__size == 1:
            return [self.__head.data]
        lst = []
        cur = self.__head
        while not (cur is self.__tail):
            lst.append(cur.data)
            cur = cur.next
        if not(self.__tail is None):
            lst.append(self.__tail.data)
        return lst
