// 角色数据接口定义
export interface Character {
  id: string;
  name: string;
  role: string;
  identity: string;
  tags: string[];
  personality: string[];

  // 功法能力
  abilities: {
    path: string;
    list: string[];
  };

  // 关键事件
  keyEvents: {
    title: string;
    description: string;
  }[];

  // 人际关系
  relationships: {
    target: string;
    label: string;
    description: string;
  }[];

  // 债务情况
  debt: {
    total: number;
    breakdown: {
      type: string;
      amount: number;
    }[];
  };

  // 修仙数据
  cultivation: {
    realm: string;
    mana: number;
    bodyStrength: number;
    realmProgress: number;
  };

  background: string;
  avatar: string;
}

// 世界观数据接口定义
export interface WorldData {
  id: string;
  name: string;
  structure: {
    aboveGround: number;
    belowGround: number;
  };
  systems: {
    currency: string;
    network: string;
    debt: string[];
  };
  layers: {
    level: number;
    name: string;
    description: string;
  }[];
}

// 导入角色数据
import characterData from './角色.json'

// 导入世界观数据
import worldData from './背景.json'

// 转换并导出角色数据
export const characters: Character[] = characterData.characters.map((char: any) => ({
  id: char.id,
  name: char.name,
  role: char.role,
  identity: char.identity,
  tags: char.tags,
  personality: char.personality,
  abilities: {
    path: char.power_system.path,
    list: char.power_system.abilities, // Map abilities array to list
  },
  keyEvents: char.key_events,
  relationships: char.relationships,
  debt: {
    total: char.id === 'zhang_yu' ? 700000 : 500000, // 张羽700k, 白真真500k
    breakdown: [
      { type: '法力贷', amount: char.id === 'zhang_yu' ? 500000 : 350000 },
      { type: '教育贷', amount: char.id === 'zhang_yu' ? 150000 : 100000 },
      { type: '修仙贷', amount: char.id === 'zhang_yu' ? 50000 : 50000 },
    ],
  },
  cultivation: {
    realm: '炼气境',
    mana: 80,
    bodyStrength: 6,
    realmProgress: 80,
  },
  background: char.background,
  avatar: `/assets/characters/${char.id}.png`, // 占位路径
}))

// 转换并导出世界观数据
export const world: WorldData = {
  id: worldData.id,
  name: worldData.name,
  structure: {
    aboveGround: 36,
    belowGround: 18,
  },
  systems: {
    currency: '灵币',
    network: '灵界网络',
    debt: ['法力贷', '教育贷', '修仙贷'],
  },
  layers: [], // 后续可以根据背景.json生成层级数据
}
