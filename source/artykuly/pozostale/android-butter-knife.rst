Android - Butter Knife
======================

Spis treści
-----------

1. Wstęp
2. Dodanie biblioteki do projektu
3. Wiązanie w aktywności
4. Wiązanie we fragmentach
5. Dodatek Android ButterKnife Zelezny


Wstęp
-----

Podczas pisania aplikacji Android, programista jest zmuszony do powtarzania tych samych fragmentów kodu podczas tworzenia powiązania elementu GUI czy zasobu z odpowiednim polem klasy. Butter Knife eliminuje ten problem - odpowiednie wiązania tworzy się używając adnotacji. Na ich podstawie, w trakcie procesu kompilacji, generowany jest odpowiedni kod. Wykorzystanie biblioteki nie wpływa znacząco na wydajność aplikacji.


Dodanie biblioteki do projektu
------------------------------

Bibliotekę dodamy do projektu poprzez modyfikację pliku `build.gradle` znajdującego się w katalogu `app`. W sekcji `dependencies` dodajemy te dwie linie (X.Y.Z należy zamienić na numer konkretnej wersji)::

    compile 'com.jakewharton:butterknife:X.Y.Z'
    annotationProcessor 'com.jakewharton:butterknife-compiler:X.Y.Z'

W nowej wersji `Gradle (od 3.0) <https://stackoverflow.com/questions/44493378/whats-the-difference-between-implementation-and-compile-in-gradle>`__ są to::

    implementation 'com.jakewharton:butterknife:X.Y.Z'
    annotationProcessor 'com.jakewharton:butterknife-compiler:X.Y.Z'

Aktualny numer wersji można sprawdzić na `stronie projektu <http://jakewharton.github.io/butterknife/>`__, w momencie pisania tego artykułu jest to 8.8.1. Poniżej przykładowy plik konfiguracyjny:

.. code-block:: text

  apply plugin: 'com.android.application'

  android {
      compileSdkVersion 26
      defaultConfig {
          applicationId "org.chyla.butterknifetestapp"
          minSdkVersion 14
          targetSdkVersion 26
          versionCode 1
          versionName "1.0"
          testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
      }
      buildTypes {
          release {
              minifyEnabled false
              proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
          }
      }
  }

  dependencies {
      implementation fileTree(dir: 'libs', include: ['*.jar'])
      implementation 'com.android.support:appcompat-v7:26.1.0'
      implementation 'com.android.support.constraint:constraint-layout:1.0.2'
      testImplementation 'junit:junit:4.12'
      androidTestImplementation 'com.android.support.test:runner:1.0.1'
      androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.1'

      implementation 'com.jakewharton:butterknife:8.8.1'
      annotationProcessor 'com.jakewharton:butterknife-compiler:8.8.1'
  }


Wiązanie w aktywności
---------------------

Tradycyjnie do utworzenia wiązania między widokiem a składnikiem klasy należy użyć metody `findViewById`, jak w poniższym przykładzie:

.. code-block:: java
  :linenos:

  public class LoginActivity extends AppCompatActivity {

      private EditText mPasswordView;

      @Override
      protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          setContentView(R.layout.activity_login);
      
          mPasswordView = (EditText) findViewById(R.id.password);
      }
  }

Każdej deklaracji (linia 3) odpowiada przypisanie widoku (linia 10). Zapis ten możemy skrócić używając `BindView`:

.. code-block:: java
  :linenos:

  public class LoginActivity extends AppCompatActivity {

      @BindView(R.id.password) EditText mPasswordView;

      @Override
      protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          setContentView(R.layout.activity_login);

          ButterKnife.bind(this);
      }

  }

Zmiany nastąpiły w linii 3 i 10. W linii 3 użyta zostałą adnotacja `BindView`, usunięty został również modyfikator dostępu `private`. W linii 10 następuje jednorazowa (dla danej klasy) inicjalizacja wiązań.

Oprócz widoków dowiązane mogą zostać zasoby:

.. code-block:: java

  public class LoginActivity extends AppCompatActivity {

      @BindString(R.string.title) String title;

      @Override
      protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          setContentView(R.layout.activity_login);

          ButterKnife.bind(this);
      }

  }

Biblioteka pozwala także powiązać przycisk z odpowiednią funkcją:

.. code-block:: java

  public class LoginActivity extends AppCompatActivity {

      @Override
      protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          setContentView(R.layout.activity_login);

          ButterKnife.bind(this);
      }

      @OnClick(R.id.email_sign_in_button)
      void attemptLogin() {
          // action
      }

      // ...

  }


Powyżej przedstawiłem, moim zdaniem, najczęściej wykorzystywane rodzaje wiązań. Zachęcam do przejrzenia `strony domowej projektu <http://jakewharton.github.io/butterknife/>`__, gdzie zostały przedstawione pozostałe rodzaje (np. wiązania grupowe).


Wiązanie we fragmentach
-----------------------

We fragmentach również istnieje możliwość stworzenia powiązania. W tym celu należy:

* do metody `bind` przekazać dodatkowy argument wskazujący na widok (na przykładzie poniżej, linia 13),
* podczas niszczenia widoku usunąć powiązanie (na przykładzie poniżej, linia 20).

Przykład wiązania utworzonego we fragmencie:

.. code-block:: java
  :linenos:

  public class SearchPhotosFragment extends Fragment {

      private Unbinder unbinder;

      @BindView(R.id.edittext_tags)
      EditText tagsEditText;

      @Override
      public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
          View view = inflater.inflate(R.layout.fragment_inspect_photos, container, false);

          unbinder = ButterKnife.bind(this, view);

          return view;
      }

      @Override public void onDestroyView() {
        super.onDestroyView();
        unbinder.unbind();
      }

      @OnClick(R.id.button_search)
      void searchPhotos() {
      }

      // ...
  }

Powód, przez który wymagana jest operacja samodzielnego usunięcia wiązania, został wyjaśniony przez *egor-n*:

    There can be a case when fragment's view is destroyed, but the fragment instance is still present. For example, when fragment goes into the back stack - `onDestroyView()` is called, but `onDestroy()` is not.
    [`egor-n <https://github.com/JakeWharton/butterknife/issues/291#issuecomment-117980043>`__]

oraz *artem-zinnatullin*:

    "System" will not clear view references in `onDestroy()`, they're just regular references and they would be freed only if GC will collect them. So for example if you have long running async code with strong reference to the Fragment, GC won't collect bonded view objects until there won't be strong references to the Fragment and you'll have memory leak which would keep not only Fragment itself but also bounded Views.

    **Calling `unbind()` in `onDestroyView()` is not required, but recommended.**

    But you should also keep in mind that if you don't prevent async callbacks that work with bounded Views after `onDestroyView()` app could be crashed by NullPointerException because of nulled View references.
    [`artem-zinnatullin <https://github.com/JakeWharton/butterknife/issues/291#issuecomment-118029002>`__]


Dodatek Android ButterKnife Zelezny
-----------------------------------

Twórcy Avasta stworzyli dodatek do IntelliJ IDEA, który automatycznie generuje pola wraz z odpowiednimi adnotacjami dla Butter Knife. Działa to bardzo podobnie, jak generowanie metod (np. setterów i getterów dla pól klasy).

W celu instalacji przechodzimy do **File** → **Settings** → **Plugins** → **Browse Repositories**, wyszukujemy *Android ButterKnife Zelezny* i instalujemy. 

.. figure:: /images/artykuly/pozostale/android-butter-knife-intellij-zelezny-install.png

    Instalacja dodatku w IntelliJ.

Poniżej animacja prezentująca działanie dodatku:

.. figure:: /images/artykuly/pozostale/android-butter-knife-intellij-zelezny-animated.gif

    Prezentacja obsługi dodatku. Źródło: [4]

.. https://github.com/avast/android-butterknife-zelezny/blob/980a2c988d7461148b92ef44c27586e318ff6098/img/zelezny_animated.gif


Literatura
----------

1. `Butter Knife <http://jakewharton.github.io/butterknife/>`__
2. `JakeWharton/butterknife: Bind Android views and callbacks to fields and methods <https://github.com/JakeWharton/butterknife>`__
3. `It's not clear if ButterKnife.unbind is required for fragments <https://github.com/JakeWharton/butterknife/issues/291>`__
4. `Android ButterKnife Zelezny :: JetBrains Plugin Repository <https://plugins.jetbrains.com/plugin/7369-android-butterknife-zelezny>`__
5. `avast/android-butterknife-zelezny: Android Studio plug-in for generating ButterKnife injections from selected layout XML. <https://github.com/avast/android-butterknife-zelezny>`__
