using System;
using System.Runtime.Remoting.Metadata.W3cXsd2001;
using System.Text.RegularExpressions;

namespace EdPractice
{
    public class Validation
    {
        public static readonly Regex DefaultNameRegexp = new Regex(@"\A(?!['-])(?!.*['-]{2})[A-Za-z'-]+(?<!['-])\z");
        public static readonly Regex DefaultEmailRegexp = new Regex(@"^[a-zA-Z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b");
        public static readonly Regex DefaultPhoneRegexp = new Regex(@"\++((380+\d{9})|(7+\d{10})|(48+\d{9}))");
        public static String InRange(dynamic value, dynamic min, dynamic max, bool inclusively = true)
        {
            string bigger = BiggerThan(value, min, inclusively);
            string less = LessThan(value, max, inclusively);
            if (string.IsNullOrEmpty(bigger) && string.IsNullOrEmpty(less))
                return "";

            return bigger + ", " + less;
        }

        public static String LessThan(dynamic value, dynamic max, bool inclusively = true)
        {
            if (inclusively)
                max += 1;
            if (value < max)
                return "";
            
            return $"Must be less than {max}";
        }
        
        public static String BiggerThan(dynamic value, dynamic min, bool inclusively = true)
        {
            if (inclusively)
                min -= 1;
            if (value > min)
                return "";
            
            return $"Must be bigger than {min}";
        }

        public static String IsName(string value, Regex nameRegexp = null)
        {
            nameRegexp ??= DefaultNameRegexp;
            if (nameRegexp.IsMatch(value))
                return "";

            return "Is not a name";
        }
        
        public static String IsEmail(string value, Regex emailRegexp = null)
        {
            emailRegexp ??= DefaultEmailRegexp;
            if (emailRegexp.IsMatch(value))
                return "";

            return "Is not an email";
        }

        public static String IsPhone(string value, Regex phoneRegexp = null)
        {
            phoneRegexp ??= DefaultPhoneRegexp;
            if (phoneRegexp.IsMatch(value))
                return "";

            return "Is not an phone";
        }
        
        public static String LengthOf(string value, int min = 0, int max = Int32.MaxValue-1, bool inclusively = true)
        {
            string bigger = BiggerThan(value.Length, min, inclusively);
            string less = LessThan(value.Length, max, inclusively);
            if (string.IsNullOrEmpty(bigger) && string.IsNullOrEmpty(less))
                return "";

            return "Length " + bigger + ", " + less;
        }
    }
}