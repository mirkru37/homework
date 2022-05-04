using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;

namespace EdPractice
{
    public class ClassCollection<T> where T : ICollectionable, ISerializable, new()
    {
        private List<T> _list = new List<T>();

        public ClassCollection()
        {
        }

        private ClassCollection(List<T> list)
        {
            _list = list;
        }

        public List<Hashtable> AddFromFile(string filePath)
        {
            List<Hashtable> errors = new List<Hashtable>();
            List<T> newRecords = new List<T>();
            bool abortion = false;
            try
            {
                using (StreamReader sr = new StreamReader(filePath))
                {
                    while (!sr.EndOfStream)
                    {
                        errors.AddRange(AddFromLine(sr.ReadLine(), false, newRecords));
                        if (errors.Count != 0)
                            abortion = true;
                    }
                }
            }
            catch (Exception e)
            {
                Hashtable error = new Hashtable();
                error.Add("File", e.Message);
                errors.Add(error);
                abortion = true;
            }

            if (!abortion)
            {
                _list.AddRange(newRecords);
            }

            return errors;
        }

        public List<Hashtable> AddFromLine(string line = null, bool save = true, List<T> newRecords = null)
        {
            if (newRecords == null)
                newRecords = new List<T>();
            List<Hashtable> errors = new List<Hashtable>();
            try
            {
                Hashtable args = readFromLine(line);
                T f = new T();
                f.create(args);
                if (!f.IsValid())
                {
                    save = false;
                    errors.Add(f.Errors());
                }
                else
                {
                    if (uniqueField("Id", newRecords.Concat(_list), f.Id))
                    {
                        newRecords.Add(f);
                    }
                    else
                    {
                        save = false;
                        Hashtable error = new Hashtable();
                        error.Add("Id", $"{f.Id} must be unique");
                        errors.Add(error);
                    }
                }
            }
            catch (IndexOutOfRangeException e)
            {
                Hashtable error = new Hashtable();
                error.Add("Base", "Wrong amount of arguments");
                errors.Add(error);
                save = false;
            }

            if (save)
                _list.AddRange(newRecords);
            return errors;
        }

        private bool uniqueField(string field, IEnumerable<T> list, int value)
        {
            var freelancers = list.ToList();
            if (freelancers.Count >= 1)
            {
                for (int i = 0; i <= freelancers.Count / 2; i++)
                {
                    var firstProp = (int) freelancers[i].GetType().GetProperty(field).GetValue(freelancers[i], null);
                    var lastProp = (int) freelancers[freelancers.Count - i - 1].GetType().GetProperty(field)
                        .GetValue(freelancers[freelancers.Count - i - 1], null);
                    if (lastProp == value || firstProp == value)
                        return false;
                }
            }

            return true;
        }

        public void PrintAll()
        {
            foreach (var f in _list)
            {
                Hashtable hash = f.SerializableHash();
                foreach (var key in hash.Keys)
                {
                    Console.WriteLine($"{key}:{hash[key]}");
                }

                Console.WriteLine();
            }
        }

        public List<Hashtable> WriteToFile(string filePath)
        {
            List<Hashtable> errors = new List<Hashtable>();
            try
            {
                File.WriteAllText(filePath, ParseFileFormat());
            }
            catch (Exception e)
            {
                Hashtable error = new Hashtable();
                error.Add("File", e.Message);
                errors.Add(error);
            }

            return errors;
        }

        public String ParseFileFormat()
        {
            string str = "";
            foreach (var f in _list)
            {
                str += $"{f}\n";
            }

            return str;
        }

        private Hashtable readFromLine(string line)
        {
            Hashtable args = new Hashtable();
            string[] values = line.Split();
            
            for (int i = 0; i < Freelancer.Fields.Length; i++)
            {
                args.Add(Freelancer.Fields[i], values[i]);
            }

            return args;
        }

        public void SortBy(string field)
        {
            _list = new List<T>(_list.OrderBy(o => o.GetType()
                .GetProperty(field)
                .GetValue(o, null)));
        }

        public ClassCollection<T> Search(string s)
        {
            List<T> result = new List<T>();
            foreach (var freelancer in _list)
            {
                if (freelancer.Contain(s))
                {
                    result.Add(freelancer);
                }
            }

            return new ClassCollection<T>(result);
        }

        public bool Delete(string val)
        {
            try
            {
                int id = Int32.Parse(val);
                _list.RemoveAll(l => l.Id == id);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public List<Hashtable> Edit(string id)
        {
            List<Hashtable> errors = new List<Hashtable>();
            try
            {
                int _id = Int32.Parse(id);
                T f = _list.First(l => l.Id == _id);
                _list.Remove(f);
                Console.WriteLine("Input values");
                string str = "Order: ";
                foreach (var field in Freelancer.Fields)
                {
                    str += field + " ";
                }

                Console.WriteLine(str);
                string val = Console.ReadLine();
                errors.AddRange(AddFromLine(val));
                if (errors.Count != 0)
                {
                    _list.Add(f);
                }
            }
            catch (Exception)
            {
                Hashtable error = new Hashtable();
                error.Add("Id", "Not found");
                errors.Add(error);
            }

            return errors;
        }
    }
}