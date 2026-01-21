import request from './request'

/**
 * 推送群组相关API
 */
export default {
  /**
   * 获取群组列表
   */
  getAll() {
    return request({
      url: '/api/push/groups',
      method: 'get'
    })
  },

  /**
   * 创建群组
   */
  create(data) {
    return request({
      url: '/api/push/groups',
      method: 'post',
      data
    })
  },

  /**
   * 更新群组
   */
  update(id, data) {
    return request({
      url: `/api/push/groups/${id}`,
      method: 'put',
      data
    })
  },

  /**
   * 删除群组
   */
  delete(id) {
    return request({
      url: `/api/push/groups/${id}`,
      method: 'delete'
    })
  },

  /**
   * 获取群组成员
   */
  getMembers(groupId) {
    return request({
      url: `/api/push/groups/${groupId}/members`,
      method: 'get'
    })
  },

  /**
   * 添加成员
   */
  addMember(groupId, employeeNo, employeeName) {
    return request({
      url: `/api/push/groups/${groupId}/members`,
      method: 'post',
      params: { employeeNo, employeeName }
    })
  },

  /**
   * 删除成员
   */
  deleteMember(groupId, memberId) {
    return request({
      url: `/api/push/groups/${groupId}/members/${memberId}`,
      method: 'delete'
    })
  }
}
