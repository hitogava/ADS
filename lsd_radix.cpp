#include <algorithm>
#include <assert.h>
#include <chrono>
#include <functional>
#include <iostream>
#include <vector>

using namespace std;

void merge(vector<string> &arr, int left, int mid, int right) {
    int i = 0;
    int j = 0;
    vector<string> buffer(arr.size());
    while ((i + left) < mid && (mid + j) < right) {
        if (arr[i + left] < arr[mid + j]) {
            buffer[i + j] = arr[i + left];
            i++;
        } else {
            buffer[i + j] = arr[j + mid];
            j++;
        }
    }
    while (i + left < mid) {
        buffer[i + j] = arr[i + left];
        i++;
    }
    while (j + mid < right) {
        buffer[i + j] = arr[j + mid];
        j++;
    }
    for (size_t k = 0; k < i + j; k++) {
        arr[left + k] = buffer[k];
    }
}

void mergeSort(vector<string> &arr, int l, int r) {
    if (r - l <= 1) {
        return;
    }
    int mid = (l + r) / 2;
    mergeSort(arr, l, mid);
    mergeSort(arr, mid, r);
    merge(arr, l, mid, r);
}

int e(int n) {
    return n;
}

int max(vector<int> &n) {
    int m = -1;
    for (size_t i = 0; i < n.size(); i++) {
        m = max(m, abs(n[i]));
    }
    return m;
}

void print_vector(vector<string> &n) {
    for (auto &e : n) {
        cout << e << endl;
    }
    cout << "\n";
}

vector<int> counting_sort(vector<int> &nums, function<int(int)> f) {
    vector<int> k(max(nums) + 1, 0);
    vector<int> sorted(nums.size(), 0);
    for (size_t i = 0; i < nums.size(); i++) {
        k[f(nums[i])] += 1;
    }
    for (size_t i = 1; i < k.size(); i++) {
        k[i] += k[i - 1];
    }
    int i = nums.size() - 1;
    int j = 0;
    while (i >= 0) {
        sorted[k[f(nums[i])] - 1] = i;
        k[f(nums[i--])]--;
    }

    return sorted;
}

vector<int> nCharOfString(vector<string> &input, int n) {
    vector<int> b{};
    for (size_t i = 0; i < input.size(); i++) {
        b.push_back(input[i][input[i].size() - n - 1]);
    }
    return b;
}

void shuffle(vector<string> &s, vector<int> indexes) {
    vector<string> buffer = s;
    for (size_t i = 0; i < s.size(); i++) {
        buffer[i] = s[indexes[i]];
    }
    s = buffer;
}

void lsd_radix_sort(vector<string> &input) {
    vector<string> buffer = input;
    if (input.size() > 1) {
        size_t wlen = input[0].size();
        for (size_t i = 0; i < wlen; i++) {
            vector<int> t = nCharOfString(buffer, i);
            t = counting_sort(t, e);
            shuffle(buffer, t);
        }
    }
    input = buffer;
}

string gen_random(const int len) {
    string alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    string tmp{};
    for (size_t i = 0; i < len; i++) {
        tmp += alpha[rand() % (alpha.length() - 1)];
    }
    return tmp;
}

bool isSorted(vector<string> vec) {
    for (size_t i = 0; i < vec.size() - 1; i++) {
        if (vec[i] > vec[i + 1])
            return false;
    }
    return true;
}

using namespace std::chrono;

void run() {
    size_t wlen = 100 + rand() % 1000;
    size_t vlen = 100 + rand() % 1000;
    vector<string> randomVec(vlen);

    for (size_t i = 0; i < vlen; i++) {
        randomVec.at(i) = gen_random(wlen);
    }
    vector<string> randomVec1 = randomVec;
    time_point<high_resolution_clock> start_point, end_point;

    start_point = high_resolution_clock::now();

    mergeSort(randomVec, 0, randomVec.size());
    assert(isSorted(randomVec));

    end_point = high_resolution_clock::now();

    auto start = time_point_cast<microseconds>(start_point).time_since_epoch().count();
    auto end = time_point_cast<microseconds>(end_point).time_since_epoch().count();
    cout << "Merge sort took " << (end - start) << " microseconds" << endl;

    start_point = high_resolution_clock::now();

    lsd_radix_sort(randomVec1);
    assert(isSorted(randomVec1));

    end_point = high_resolution_clock::now();
    start = time_point_cast<microseconds>(start_point).time_since_epoch().count();
    end = time_point_cast<microseconds>(end_point).time_since_epoch().count();
    cout << "Radix sort took " << (end - start) << " microseconds " << endl;
}

void bench() {
    run();
}

int main() {
    srand((unsigned) time(NULL));
    bench();
    return 0;
}
