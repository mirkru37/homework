using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace EdPractice
{
    public class Freelancer : ISerializable
    {
        public static readonly String[] AvailablePositions = { "DevOps", "BackEnd", "QA", "Tester" };
        public static readonly String[] Fields = { "Id", "Name", "Email", "PhoneNumber", "Availability", "Salary", "Position" };
        
        private int id;
        private String name;
        private String email;
        private String phone_number;
        private int availability; // hr/week
        private double salary;
        private String position;
        private Hashtable errors = new Hashtable();
        
        public int Id
        {
            get => id;
            set
            {
                string valid = Validation.InRange(value, 0, Int32.MaxValue-1);
                if (String.IsNullOrEmpty(valid))
                {
                    id = value;
                    errors.Remove("Id");
                }
                else
                    errors.Add("Id", valid);
            }
        }

        public string Name
        {
            get => name;
            set
            {
                string validName = Validation.IsName(value);
                string validLength = Validation.LengthOf(value, 2, 20);
                if (String.IsNullOrEmpty(validName) && String.IsNullOrEmpty(validLength))
                {
                    name = value;
                    errors.Remove("Name");
                }
                else
                    errors.Add("Name", validLength + ", " + validName);
            }
        }

        public string Email
        {
            get => email;
            set
            {
                string validEmail = Validation.IsEmail(value);
                if (String.IsNullOrEmpty(validEmail))
                {
                    email = value;
                    errors.Remove("Email");
                }
                else
                    errors.Add("Email", validEmail);
            }
        }

        public string PhoneNumber
        {
            get => phone_number;
            set
            {
                string validPhone = Validation.IsPhone(value);
                if (String.IsNullOrEmpty(validPhone))
                {
                    phone_number = value;
                    errors.Remove("PhoneNumber");
                }
                else
                    errors.Add("PhoneNumber", validPhone);
            }
        }

        public int Availability
        {
            get => availability;
            set
            {
                string valid = Validation.InRange(value, 0, 24*7);
                if (String.IsNullOrEmpty(valid))
                {
                    availability = value;
                    errors.Remove("Availability");
                }
                else
                    errors.Add("Availability", valid);
            }
        }

        public double Salary
        {
            get => salary;
            set
            {
                string valid = Validation.InRange(value, 0, float.MaxValue - 1);
                if (String.IsNullOrEmpty(valid))
                {
                    salary = Math.Round(value, 2);
                    errors.Remove("Salary");
                }
                else
                    errors.Add("Salary", valid);
            }
        }

        public string Position
        {
            get => position;
            set
            {
                if (AvailablePositions.Contains(value))
                {
                    position = value;
                    errors.Remove("Position");
                }
                else
                    errors.Add("Position", "Is not a valid position");
            }
        }

        public Freelancer(Hashtable htParams)
        {
            foreach (var field in GetType().GetProperties())
            {
                try
                {
                    var param = Convert.ChangeType(htParams[field.Name], field.PropertyType);
                    field.SetValue(this, param, null);
                }  
                catch (FormatException e)
                {
                    errors.Add(field.Name, e.Message);
                }
            }
        }

        public Hashtable SerializableHash()
        {
            Hashtable data = new Hashtable();
            foreach (var field in GetType().GetProperties())
            {
                data.Add(field.Name, field.GetValue(this, null));
            }

            return data;
        }

        public override String ToString()
        {
            string str = "";
            foreach (var field in Fields)
            {
                str += $"{GetType().GetProperty(field).GetValue(this, null)} ";
            }

            return str;
        }
        public bool IsValid()
        {
            return !Convert.ToBoolean(errors.Count);
        }

        public Hashtable Errors()
        {
            return errors;
        }

        public bool Contain(string s)
        {
            bool res = false;
            string str = "";
            foreach (var field in Fields)
            {
                str += $"{GetType().GetProperty(field).GetValue(this, null)}";
                res = res || str.ToLower().Contains(s.ToLower());
            }

            return res;
        }
    }
}