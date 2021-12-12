int findDuplicate(int* nums, int n){
    //i->nums[i]  n个点 n+1条有向边必产生环
    int fast = 0, slow = 0;
    do {
        fast = nums[nums[fast]];
        slow = nums[slow];
    }while (fast != slow); //第一次相遇不一定是入度大于1的点
    fast = 0;
    do {
        fast = nums[fast];
        slow = nums[slow];
    } while (fast != slow); //继续走c步
    
    return slow;
}
