import request from './request'

/**
 * 推送配置相关API
 */
export default {
  /**
   * 获取业务配置
   */
  getBusinessConfig(businessCode) {
    return request({
      url: `/api/push/config/business/${businessCode}`,
      method: 'get'
    })
  },

  /**
   * 保存或更新配置
   */
  saveConfig(data) {
    return request({
      url: '/api/push/config',
      method: 'post',
      data
    })
  },

  /**
   * 删除配置
   */
  deleteConfig(id) {
    return request({
      url: `/api/push/config/${id}`,
      method: 'delete'
    })
  },

  /**
   * 获取所有业务类型
   */
  getBusinessTypes() {
    return request({
      url: '/api/push/config/business-types',
      method: 'get'
    })
  },

  /**
   * 根据ID获取业务类型
   */
  getBusinessTypeById(id) {
    return request({
      url: `/api/push/config/business-types/${id}`,
      method: 'get'
    })
  },

  /**
   * 创建业务类型
   */
  createBusinessType(data) {
    return request({
      url: '/api/push/config/business-types',
      method: 'post',
      data
    })
  },

  /**
   * 更新业务类型
   */
  updateBusinessType(id, data) {
    return request({
      url: `/api/push/config/business-types/${id}`,
      method: 'put',
      data
    })
  },

  /**
   * 删除业务类型
   */
  deleteBusinessType(id) {
    return request({
      url: `/api/push/config/business-types/${id}`,
      method: 'delete'
    })
  }
}
