using System.Collections;
using System.Collections.Generic;
using System.IO.Ports;

namespace EdPractice
{
    public interface ICollectionable
    {
        bool IsValid();

        Hashtable Errors();

        int Id
        {
            get;
            set;
        }

        string[] GetFields();

        bool Contain(string s);

        void create(Hashtable args);
    }
}