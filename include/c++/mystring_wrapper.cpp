#include "C:\Users\lyuga\AppData\Local\Programs\Python\Python311\Lib\site-packages\pybind11\include\pybind11\pybind11.h"
#include "MyString.h"

namespace py = pybind11;

PYBIND11_MODULE(MyString, m) {
    py::class_<MyString>(m, "MyString")
        .def(py::init<>())
        .def(py::init<int, char>())
        .def(py::init<char*, int>())
        .def(py::init<const MyString&>())
        .def(py::init<char*>())
        .def(py::init<std::string>())

        .def("capacity", &MyString::capacity)
        .def("shrink_to_fit", &MyString::shrink_to_fit)

        .def("length", &MyString::length)
        .def("__len__", &MyString::length)
        .def("size", &MyString::size)

        .def("c_str", &MyString::c_str)
        .def("data", &MyString::data)

        .def("empty", &MyString::empty)

        .def("insert", [](MyString& self, int index, char* sub) { self.insert(index, sub); })
        .def("insert", [](MyString& self, int index, int count, char c) { self.insert(index, count, c); })
        .def("insert", [](MyString& self, int index, string str) { self.insert(index, str); })
        .def("insert", [](MyString& self, int index, string str, int count) { self.insert(index, str, count); })

        .def("append", [](MyString& self, int n,  char c) { self.append(n, c); })
        .def("append", [](MyString& self, char* str) { self.append(str); })
        .def("append", [](MyString& self, string str) { self.append(str); })
        .def("append", [](MyString& self, char* str, int index, int count) { self.append(str, index, count); })
        .def("append", [](MyString& self, string str_to_append, int index, int count) { self.append(str_to_append, index, count); })

        .def("replace", [](MyString& self, int index, int count, string str) { self.replace(index, count, str); })

        .def("find", [](MyString& self, char* str, int count) { return self.find(str, count); })
        .def("find", [](MyString& self, char* str) { return self.find(str); })
        .def("find", [](MyString& self, string str) { return self.find(str); })
        .def("find", [](MyString& self, string str, int index) { return self.find(str, index); })

        .def("clear", &MyString::clear)
        .def("erase", &MyString::erase)

        .def("substr", (MyString (MyString::*)(int)) &MyString::substr)
        .def("substr", (MyString (MyString::*)(int, int)) &MyString::substr)
        
        .def("__eq__", (bool (MyString::*)(const MyString&)) &MyString::operator==)
        .def("__ne__", (bool (MyString::*)(const MyString&)) &MyString::operator!=)
        .def("__gt__", (bool (MyString::*)(const MyString&)) &MyString::operator>)
        .def("__ge__", (bool (MyString::*)(const MyString&)) &MyString::operator>=)
        .def("__lt__", (bool (MyString::*)(const MyString&)) &MyString::operator<)
        .def("__le__", (bool (MyString::*)(const MyString&)) &MyString::operator<=)

        .def("__getitem__", (char& (MyString::*)(int)) &MyString::operator[])
        .def("__add__", (MyString (MyString::*)(MyString&)) &MyString::operator+)
        .def("__add__", (MyString (MyString::*)(char*)) &MyString::operator+)
        .def("__add__", (MyString (MyString::*)(std::string)) &MyString::operator+)

        .def("__iadd__", (MyString& (MyString::*)(char*)) &MyString::operator+=)
        .def("__iadd__", (MyString& (MyString::*)(std::string)) &MyString::operator+=)
        .def("__iadd__", (MyString& (MyString::*)(MyString &str)) &MyString::operator+=)
        
        .def("__setitem__", (MyString& (MyString::*)(int, char)) &MyString::operator[])
        
        .def("__str__", &MyString::c_str)
        .def("__repr__", &MyString::c_str)

        .def("__repr__", [](const MyString& str) { return str.c_str(); });
}